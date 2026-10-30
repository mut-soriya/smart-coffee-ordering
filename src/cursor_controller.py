import math
import time


class CursorController:
    def __init__(
        self,
        screen_width=1280,
        screen_height=720,
        margin=0.08,
        min_cutoff=1.2,
        beta=0.015,
        derivative_cutoff=1.0,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin = margin
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.derivative_cutoff = derivative_cutoff
        self.cursor_x = screen_width / 2
        self.cursor_y = screen_height / 2
        self._last_time = None
        self._last_raw_x = None
        self._last_raw_y = None
        self._filtered_dx = 0.0
        self._filtered_dy = 0.0
        self._initialized = False

    @staticmethod
    def _alpha(cutoff, dt):
        tau = 1 / (2 * math.pi * cutoff)
        return 1 / (1 + tau / dt)

    def _filter_axis(self, target, current, last_raw, filtered_derivative, dt):
        raw_derivative = 0.0 if last_raw is None else (target - last_raw) / dt
        derivative_alpha = self._alpha(self.derivative_cutoff, dt)
        filtered_derivative += derivative_alpha * (raw_derivative - filtered_derivative)
        cutoff = self.min_cutoff + self.beta * abs(filtered_derivative)
        alpha = self._alpha(cutoff, dt)
        return current + alpha * (target - current), filtered_derivative

    def update(self, hand_landmarks, timestamp=None):
        if not hand_landmarks:
            return self.get_position()

        point = hand_landmarks[8]
        return self.update_point(point.x, point.y, timestamp)

    def update_point(self, x, y, timestamp=None):
        if not math.isfinite(x) or not math.isfinite(y):
            return self.get_position()

        usable_range = 1 - self.margin * 2
        normalized_x = max(0, min(1, (x - self.margin) / usable_range))
        normalized_y = max(0, min(1, (y - self.margin) / usable_range))
        target_x = normalized_x * self.screen_width
        target_y = normalized_y * self.screen_height
        now = time.monotonic() if timestamp is None else timestamp

        if not self._initialized:
            self.cursor_x = target_x
            self.cursor_y = target_y
            self._last_raw_x = target_x
            self._last_raw_y = target_y
            self._last_time = now
            self._initialized = True
            return self.get_position()

        dt = max(1 / 120, min(0.1, now - self._last_time))
        self.cursor_x, self._filtered_dx = self._filter_axis(
            target_x,
            self.cursor_x,
            self._last_raw_x,
            self._filtered_dx,
            dt,
        )
        self.cursor_y, self._filtered_dy = self._filter_axis(
            target_y,
            self.cursor_y,
            self._last_raw_y,
            self._filtered_dy,
            dt,
        )
        self.cursor_x = max(0, min(self.screen_width, self.cursor_x))
        self.cursor_y = max(0, min(self.screen_height, self.cursor_y))
        self._last_raw_x = target_x
        self._last_raw_y = target_y
        self._last_time = now
        return self.get_position()

    def get_position(self):
        return round(self.cursor_x), round(self.cursor_y)

    def set_position(self, x, y):
        self.cursor_x = max(0, min(self.screen_width, x))
        self.cursor_y = max(0, min(self.screen_height, y))

    def reset(self):
        self.cursor_x = self.screen_width / 2
        self.cursor_y = self.screen_height / 2
        self._last_time = None
        self._last_raw_x = None
        self._last_raw_y = None
        self._filtered_dx = 0.0
        self._filtered_dy = 0.0
        self._initialized = False
