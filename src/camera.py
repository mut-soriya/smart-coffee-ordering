import cv2

class Camera:
    def __init__(self, camera_index=0, width=1280, height=720, fps=60):
        self.camera_index=camera_index; self.width=width; self.height=height; self.fps=fps; self.cap=None
    def start(self):
        self.cap=cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened(): raise RuntimeError("Could not open camera.")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,self.width); self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,self.height)
        self.cap.set(cv2.CAP_PROP_FPS,self.fps); self.cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
    def read(self):
        if self.cap is None: raise RuntimeError("Camera has not been started.")
        ok,frame=self.cap.read(); return frame if ok else None
    def release(self):
        if self.cap is not None: self.cap.release(); self.cap=None
    def is_opened(self): return self.cap is not None and self.cap.isOpened()
