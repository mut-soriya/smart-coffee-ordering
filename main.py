import asyncio
import json
import threading
import time
import webbrowser
from datetime import datetime
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit

import cv2
from websockets.asyncio.server import serve

from src.camera import Camera
from src.hand_tracker import HandTracker
from src.gesture_engine import GestureEngine
from src.cursor_controller import CursorController
from src.menu_manager import MenuManager
from src.cart import Cart
from src.order_manager import OrderManager
from src.kitchen_queue import KitchenQueue
from src.config import HAND_MODEL_PATH, SCREEN_WIDTH, SCREEN_HEIGHT, FPS

ROOT = Path(__file__).resolve().parent
FRONTEND = ROOT / "frontend"
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8000
WS_HOST = "127.0.0.1"
WS_PORT = 8765


class KioskHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, app=None, **kwargs):
        self.app = app
        super().__init__(*args, directory=str(FRONTEND), **kwargs)

    def do_GET(self):
        if urlsplit(self.path).path != "/camera-preview":
            super().do_GET()
            return

        frame = None
        startup_deadline = time.monotonic() + 5
        while self.app.running and frame is None and time.monotonic() < startup_deadline:
            with self.app.camera_frame_lock:
                frame = self.app.latest_camera_jpeg
            if frame is None:
                time.sleep(0.05)
        if frame is None:
            self.send_error(503, "Camera preview is not available")
            return

        self.send_response(200)
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Connection", "close")
        self.end_headers()
        while self.app.running:
            try:
                self.wfile.write(b"--frame\r\nContent-Type: image/jpeg\r\n")
                self.wfile.write(f"Content-Length: {len(frame)}\r\n\r\n".encode("ascii"))
                self.wfile.write(frame + b"\r\n")
                self.wfile.flush()
            except (BrokenPipeError, ConnectionAbortedError, ConnectionResetError):
                break
            time.sleep(1 / 60)
            with self.app.camera_frame_lock:
                frame = self.app.latest_camera_jpeg

    def translate_path(self, path):
        request_path = unquote(urlsplit(path).path)
        if request_path == "/assets" or request_path.startswith("/assets/"):
            assets_root = (ROOT / "assets").resolve()
            asset_path = (ROOT / request_path.lstrip("/\\")).resolve()
            try:
                asset_path.relative_to(assets_root)
            except ValueError:
                return str(assets_root / "__not_found__")
            return str(asset_path)
        return super().translate_path(path)

    def log_message(self, fmt, *args):
        pass


class SmartCoffeeWebApp:
    """Python CV + ordering backend for the HTML/CSS/JS kiosk."""

    def __init__(self):
        self.menu = MenuManager(str(ROOT / "data" / "menu.json"))
        self.cart = Cart()
        self.orders = OrderManager()
        self.kitchen = KitchenQueue(self.orders)
        self.camera = Camera(width=1280, height=720)
        self.tracker = HandTracker(str(HAND_MODEL_PATH))
        self.gesture = GestureEngine()
        self.cursor_controller = CursorController(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
            margin=0.08,
            min_cutoff=0.9,
            beta=0.01,
        )

        self.running = True
        self.camera_ok = False
        self.hand_detected = False
        self.last_gesture = "NONE"
        self.cursor = {"x": SCREEN_WIDTH // 2, "y": SCREEN_HEIGHT // 2}
        self.ws_loop = None
        self.clients = set()
        self.lock = threading.Lock()
        self.camera_frame_lock = threading.Lock()
        self.latest_camera_jpeg = None

    # ---------------- WebSocket ----------------
    async def ws_handler(self, connection):
        self.clients.add(connection)
        try:
            await connection.send(json.dumps(self.state_message()))
            async for raw in connection:
                try:
                    message = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                await self.handle_message(message)
        finally:
            self.clients.discard(connection)

    async def handle_message(self, message):
        msg_type = message.get("type")

        try:
            if msg_type == "hello":
                await self.broadcast(self.state_message())

            elif msg_type == "cart_add":
                item = message.get("item") or {}
                product = self.menu.get_product(item.get("pid"))
                if not product:
                    await self.send_error("Product not found")
                    return

                customization = self.ui_item_to_customization(item)
                edit_index = message.get("editIndex")
                if edit_index is not None and int(edit_index) >= 0:
                    idx = int(edit_index)
                    if idx < len(self.cart.items):
                        self.cart.items[idx].product = product
                        self.cart.items[idx].quantity = max(1, int(item.get("qty", 1)))
                        self.cart.items[idx].customization = customization
                    else:
                        self.cart.add_item(product, item.get("qty", 1), customization)
                else:
                    self.cart.add_item(product, item.get("qty", 1), customization)
                await self.broadcast(self.cart_message())

            elif msg_type == "cart_update":
                self.cart.update_quantity(int(message.get("index", -1)), int(message.get("delta", 0)))
                await self.broadcast(self.cart_message())

            elif msg_type == "cart_remove":
                self.cart.remove_item(int(message.get("index", -1)))
                await self.broadcast(self.cart_message())

            elif msg_type == "confirm_order":
                if self.cart.is_empty():
                    await self.send_error("Cart is empty")
                    return
                order = self.orders.create_order(self.cart)
                await self.broadcast({"type": "order_created", "order": self.order_to_ui(order)})

            elif msg_type == "reset_session":
                self.cart.clear()
                await self.broadcast(self.cart_message())

            elif msg_type == "kitchen_update":
                oid = message.get("orderId")
                order = self.orders.get_order(oid)
                if order:
                    if order.status == "PENDING":
                        self.kitchen.start_order(oid)
                    elif order.status == "PREPARING":
                        self.kitchen.mark_order_ready(oid)
                    elif order.status == "READY":
                        self.kitchen.complete_order(oid)
                    await self.broadcast(self.kitchen_message())

        except Exception as exc:
            await self.send_error(str(exc))

    async def send_error(self, message):
        await self.broadcast({"type": "error", "message": message})

    async def broadcast(self, message):
        if not self.clients:
            return
        payload = json.dumps(message)
        dead = []
        for client in list(self.clients):
            try:
                await client.send(payload)
            except Exception:
                dead.append(client)
        for client in dead:
            self.clients.discard(client)

    def broadcast_threadsafe(self, message):
        if self.ws_loop and self.ws_loop.is_running():
            asyncio.run_coroutine_threadsafe(self.broadcast(message), self.ws_loop)

    # ---------------- Data conversion ----------------
    def ui_item_to_customization(self, item):
        product = self.menu.get_product(item.get("pid"))
        size_idx = int(item.get("size", 0))
        temp_idx = int(item.get("temp", 0))
        sugar_idx = int(item.get("sugar", 0))
        milk_idx = int(item.get("milk", 0))
        add_indices = item.get("add", []) or []

        size = product.sizes[size_idx] if product.sizes and size_idx < len(product.sizes) else ""
        temperature = product.temperatures[temp_idx] if product.temperatures and temp_idx < len(product.temperatures) else ""
        sugar = product.sugar_levels[sugar_idx] if product.sugar_levels and sugar_idx < len(product.sugar_levels) else ""
        milk = product.milk_options[milk_idx] if product.milk_options and milk_idx < len(product.milk_options) else ""
        toppings = [product.toppings[i] for i in add_indices if i < len(product.toppings)]

        extra = 0.0
        if milk in ("Oat", "Almond"):
            extra += 0.30
        extra += 0.50 * len(toppings)

        return {
            "size": size,
            "temperature": temperature,
            "sugar": sugar,
            "milk": milk,
            "toppings": toppings,
            "extra_price": extra,
            "ui": {
                "size": size_idx,
                "temp": temp_idx,
                "sugar": sugar_idx,
                "milk": milk_idx,
                "add": add_indices,
            },
        }

    def cart_ui(self):
        result = []
        for item in self.cart.items:
            c = item.customization or {}
            ui = c.get("ui", {})
            result.append({
                "pid": item.product.product_id,
                "size": ui.get("size", 0),
                "temp": ui.get("temp", 0),
                "sugar": ui.get("sugar", 0),
                "milk": ui.get("milk", 0),
                "add": list(ui.get("add", [])),
                "qty": item.quantity,
            })
        return result

    def cart_message(self):
        return {
            "type": "cart_sync",
            "cart": self.cart_ui(),
            "subtotal": self.cart.get_subtotal(),
            "total": self.cart.get_total(),
        }

    def order_to_ui(self, order):
        items = []
        for item in order.items:
            c = item.customization or {}
            ui = c.get("ui", {})
            items.append({
                "pid": item.product.product_id,
                "qty": item.quantity,
                "size": ui.get("size", 0),
                "temp": ui.get("temp", 0),
                "sugar": ui.get("sugar", 0),
                "milk": ui.get("milk", 0),
                "add": list(ui.get("add", [])),
                "product": {
                    "id": item.product.product_id,
                    "name": item.product.name,
                    "price": item.product.price,
                },
                "customization": c,
                "subtotal": item.get_subtotal(),
            })
        now = order.created_at
        return {
            "id": order.order_id,
            "order_id": order.order_id,
            "items": items,
            "subtotal": order.subtotal,
            "total": order.total,
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "d": now.strftime("%d %b %Y"),
            "t": now.strftime("%I:%M %p"),
        }

    def kitchen_message(self):
        def col(items):
            return [{"id": o.order_id, "status": o.status, "total": o.total,
                     "items": [{"name": i.product.name, "quantity": i.quantity} for i in o.items]}
                    for o in items]
        return {"type": "kitchen_sync", "pending": col(self.kitchen.get_pending()),
                "preparing": col(self.kitchen.get_preparing()), "ready": col(self.kitchen.get_ready())}

    def state_message(self):
        return {
            "type": "state",
            "camera": "ok" if self.camera_ok else "e",
            "handDetected": self.hand_detected,
            "cursor": self.cursor,
            "gesture": self.last_gesture,
            "gestureConfidence": self.gesture.confidence,
            "gestureDetails": self.gesture.details,
            "gestureCandidate": self.gesture.candidate_gesture,
            "fingerStates": self.gesture.finger_states,
            "cart": self.cart_ui(),
        }

    # ---------------- Camera / CV ----------------
    def process_camera(self):
        frame = self.camera.read()
        if frame is None:
            self.hand_detected = False
            self.last_gesture = "NONE"
            self.gesture.reset_tracking()
            return None

        frame = cv2.flip(frame, 1)
        results = self.tracker.process(frame)
        self.hand_detected = bool(results.hand_landmarks)

        if results.hand_landmarks:
            hand = results.hand_landmarks[0]
            self.last_gesture = self.gesture.detect(
                hand,
                aspect_ratio=frame.shape[1] / frame.shape[0],
            )
            if self.last_gesture == GestureEngine.TWO_FINGER_SCROLL:
                cursor_point = (
                    (hand[8].x + hand[12].x) / 2,
                    (hand[8].y + hand[12].y) / 2,
                )
                x, y = self.cursor_controller.update_point(*cursor_point)
            else:
                x, y = self.cursor_controller.update(hand)
            self.cursor = {"x": x, "y": y}
        else:
            self.last_gesture = "NONE"
            self.gesture.reset_tracking()

        return self.tracker.draw_landmarks(frame, results)

    def camera_loop(self):
        try:
            self.camera.start()
            self.camera_ok = True
            self.broadcast_threadsafe({"type": "state", "camera": "ok", "handDetected": False, "cursor": self.cursor, "gesture": "NONE"})
        except Exception as exc:
            self.camera_ok = False
            print("CAMERA ERROR:", exc)
            self.broadcast_threadsafe({"type": "state", "camera": "e", "handDetected": False, "cursor": self.cursor, "gesture": "NONE"})
            while self.running:
                time.sleep(0.5)
            return

        while self.running:
            frame = self.process_camera()
            if frame is not None:
                cv2.putText(frame, f"Gesture: {self.last_gesture}", (20, 35),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 220, 120), 2)
                cv2.putText(
                    frame,
                    f"{self.gesture.details} | {self.gesture.confidence:.0%}",
                    (20, 68),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 220, 120),
                    2,
                )
                finger_status = "Fingers: " + "  ".join(
                    f"{name[0].upper()}:{'UP' if extended else 'DOWN'}"
                    for name, extended in self.gesture.finger_states.items()
                )
                if self.gesture.finger_states:
                    cv2.putText(
                        frame,
                        finger_status,
                        (20, 98),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (180, 240, 180),
                        1,
                    )
                cv2.putText(frame, "MIRRORED CAMERA | Q = quit", (20, 125),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.imshow("Smart Coffee - Computer Vision", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.running = False

                preview_frame = cv2.resize(frame, (640, 360))
                encoded, jpeg = cv2.imencode(
                    ".jpg",
                    preview_frame,
                    [cv2.IMWRITE_JPEG_QUALITY, 75],
                )
                if encoded:
                    with self.camera_frame_lock:
                        self.latest_camera_jpeg = jpeg.tobytes()

            self.broadcast_threadsafe({
                "type": "state",
                "camera": "ok" if self.camera_ok else "e",
                "handDetected": self.hand_detected,
                "cursor": self.cursor,
                "gesture": self.last_gesture,
                "gestureConfidence": self.gesture.confidence,
                "gestureDetails": self.gesture.details,
                "gestureCandidate": self.gesture.candidate_gesture,
                "fingerStates": self.gesture.finger_states,
            })
    # ---------------- Servers ----------------
    def http_server(self):
        handler = partial(KioskHTTPRequestHandler, app=self)
        server = ThreadingHTTPServer((HTTP_HOST, HTTP_PORT), handler)
        server.timeout = 0.5
        while self.running:
            server.handle_request()
        server.server_close()

    def websocket_server(self):
        async def run():
            self.ws_loop = asyncio.get_running_loop()
            async with serve(self.ws_handler, WS_HOST, WS_PORT, max_size=2**20):
                await asyncio.Future()
        asyncio.run(run())

    def start(self):
        print("=" * 64)
        print("SMART COFFEE ORDERING — WEB KIOSK")
        print("=" * 64)
        print(f"UI:       http://{HTTP_HOST}:{HTTP_PORT}")
        print(f"WebSocket: ws://{WS_HOST}:{WS_PORT}")
        print("Camera:   mirrored + MediaPipe hand tracking")
        print("Cursor:   index fingertip")
        print("=" * 64)

        http_thread = threading.Thread(target=self.http_server, daemon=True)
        ws_thread = threading.Thread(target=self.websocket_server, daemon=True)
        http_thread.start()
        ws_thread.start()

        try:
            time.sleep(0.8)
            webbrowser.open(f"http://{HTTP_HOST}:{HTTP_PORT}")
            self.camera_loop()
        except Exception as exc:
            print("APPLICATION ERROR:", exc)
            import traceback
            traceback.print_exc()
        finally:
            self.running = False
            try:
                self.camera.release()
            except Exception:
                pass
            try:
                self.tracker.close()
            except Exception:
                pass
            cv2.destroyAllWindows()
            print("Smart Coffee closed.")


def main():
    SmartCoffeeWebApp().start()


if __name__ == "__main__":
    main()
