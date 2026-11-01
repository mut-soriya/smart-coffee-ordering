import math
import time


class GestureEngine:
    POINT = "POINT"
    FIST = "FIST"
    PINCH = "PINCH"
    TWO_FINGER_SCROLL = "TWO_FINGER_SCROLL"
    RELAX = "RELAX"
    NONE = "NONE"

    FINGERS = (
        ("index", 5, 6, 7, 8),
        ("middle", 9, 10, 11, 12),
        ("ring", 13, 14, 15, 16),
        ("pinky", 17, 18, 19, 20),
    )

    def __init__(
        self,
        pinch_threshold=0.38,
        pinch_release_threshold=0.60,
        stability_frames=2,
        fist_hold_duration=0.4,
    ):
        self.pinch_threshold = pinch_threshold
        self.pinch_release_threshold = max(
            pinch_threshold,
            pinch_release_threshold,
        )
        self.stability_frames = stability_frames
        self.fist_hold_duration = fist_hold_duration
        self.last_gesture = self.NONE
        self.confidence = 0.0
        self.details = "Show your hand to the camera"
        self.finger_states = {}
        self._candidate_gesture = self.NONE
        self._candidate_frames = 0
        self._candidate_started_at = None
        self._candidate_elapsed = 0.0
        self.is_pinching = False
        self._fist_latched = False
        self._non_fist_frames = 0

    @staticmethod
    def _dist(a, b, aspect_ratio=1.0):
        return math.hypot((a.x - b.x) * aspect_ratio, a.y - b.y)

    @staticmethod
    def _angle(a, b, c, aspect_ratio=1.0):
        ab = ((a.x - b.x) * aspect_ratio, a.y - b.y)
        cb = ((c.x - b.x) * aspect_ratio, c.y - b.y)
        lengths = math.hypot(*ab) * math.hypot(*cb)
        if lengths < 1e-8:
            return 0.0
        cosine = (ab[0] * cb[0] + ab[1] * cb[1]) / lengths
        return math.degrees(math.acos(max(-1.0, min(1.0, cosine))))

    @classmethod
    def _finger_extension(cls, hand, mcp, pip, dip, tip, aspect_ratio):
        straight_angle = cls._angle(
            hand[mcp],
            hand[pip],
            hand[dip],
            aspect_ratio,
        )
        tip_distance = cls._dist(hand[0], hand[tip], aspect_ratio)
        pip_distance = cls._dist(hand[0], hand[pip], aspect_ratio)
        extension_ratio = tip_distance / max(pip_distance, 1e-5)
        extended = straight_angle >= 120 and extension_ratio >= 1.0
        angle_score = max(0.0, min(1.0, (straight_angle - 100) / 55))
        length_score = max(0.0, min(1.0, (extension_ratio - 0.85) / 0.3))
        return extended, min(angle_score, length_score), straight_angle

    def _update_candidate(self, gesture, confidence, details, now=None, min_duration=0):
        if gesture == self._candidate_gesture:
            self._candidate_frames += 1
        else:
            self._candidate_gesture = gesture
            self._candidate_frames = 1
            self._candidate_started_at = now

        self.confidence = confidence
        elapsed = 0 if self._candidate_started_at is None else now - self._candidate_started_at
        self._candidate_elapsed = elapsed
        if (
            gesture == self.NONE
            or self._candidate_frames < self.stability_frames
            or elapsed < min_duration
        ):
            self.last_gesture = self.NONE
            self.details = f"Stabilizing {gesture.lower().replace('_', ' ')}"
            return self.NONE

        self.last_gesture = gesture
        self.details = details
        return gesture

    def detect(self, hand, timestamp=None, aspect_ratio=1.0):
        if hand is None or len(hand) < 21:
            self.reset_tracking()
            return self.NONE

        now = time.monotonic() if timestamp is None else timestamp

        palm_scale = self._dist(hand[0], hand[9], aspect_ratio)
        self.finger_states = {}
        scores = []
        for name, mcp, pip, dip, tip in self.FINGERS:
            is_extended, score, _angle = self._finger_extension(
                hand,
                mcp,
                pip,
                dip,
                tip,
                aspect_ratio,
            )
            self.finger_states[name] = is_extended
            scores.append(score)

        extended_count = sum(self.finger_states.values())
        thumb_tip_to_palm = self._dist(
            hand[4],
            hand[9],
            aspect_ratio,
        ) / max(palm_scale, 0.04)
        thumb_tip_to_index = self._dist(
            hand[4],
            hand[5],
            aspect_ratio,
        ) / max(palm_scale, 0.04)
        thumb_tucked = (
            thumb_tip_to_palm < 0.90
            or thumb_tip_to_index < 0.85
        )
        two_fingers_up = (
            self.finger_states["index"]
            and self.finger_states["middle"]
            and not self.finger_states["ring"]
            and not self.finger_states["pinky"]
        )

        index_mcp_to_tip = self._dist(hand[5], hand[8], aspect_ratio) / max(palm_scale, 0.04)
        middle_mcp_to_tip = self._dist(hand[9], hand[12], aspect_ratio) / max(palm_scale, 0.04)

        is_fist_candidate = (
            extended_count <= 1
            and not self.finger_states["index"]
            and index_mcp_to_tip < 0.65
            and middle_mcp_to_tip < 0.65
            and (thumb_tucked or extended_count == 0)
        )

        pinch_ratio = self._dist(hand[4], hand[8], aspect_ratio) / max(
            palm_scale,
            0.04,
        )
        if self.is_pinching:
            if pinch_ratio <= self.pinch_release_threshold and not is_fist_candidate:
                self.last_gesture = self.PINCH
                self.confidence = max(0.0, min(1.0, 1 - pinch_ratio / self.pinch_release_threshold))
                self.details = f"Pinch held · thumb/index {pinch_ratio:.2f}× palm length"
                return self.PINCH
            self.is_pinching = False
            self._candidate_gesture = self.NONE
            self._candidate_frames = 0
            self._candidate_started_at = None

        if is_fist_candidate:
            self._non_fist_frames = 0
            confidence = (1 - sum(scores) / len(scores)) * (
                0.7 + 0.3 * (1 - extended_count / 2)
            )
            result = self._update_candidate(
                self.FIST,
                confidence,
                f"Fist · {4 - extended_count}/4 fingers curled",
                now,
                self.fist_hold_duration,
            )
            if result == self.FIST:
                if self._fist_latched:
                    self.last_gesture = self.NONE
                    self.details = "Fist held · release to reset"
                    return self.NONE
                self._fist_latched = True
                return self.FIST
            return result

        self._non_fist_frames += 1
        if self._non_fist_frames >= self.stability_frames:
            self._fist_latched = False

        if pinch_ratio < self.pinch_threshold and index_mcp_to_tip >= 0.50:
            confidence = max(0.0, min(1.0, 1 - pinch_ratio / self.pinch_threshold))
            result = self._update_candidate(
                self.PINCH,
                confidence,
                f"Pinch · thumb/index {pinch_ratio:.2f}× palm length",
                now,
            )
            if result == self.PINCH:
                self.is_pinching = True
            return result

        three_fingers_up = (
            self.finger_states["index"]
            and self.finger_states["middle"]
            and self.finger_states["ring"]
            and not self.finger_states["pinky"]
        )
        if three_fingers_up:
            confidence = min(scores[0], scores[1], scores[2], 1 - scores[3])
            return self._update_candidate(
                self.RELAX,
                confidence,
                "Relax · hold-to-select paused",
                now,
            )

        if two_fingers_up:
            confidence = min(
                scores[0],
                scores[1],
                1 - scores[2],
                1 - scores[3],
            )
            return self._update_candidate(
                self.TWO_FINGER_SCROLL,
                confidence,
                "Two-finger scroll · index and middle fingers extended",
                now,
            )

        if self.finger_states["index"] and extended_count <= 2:
            confidence = scores[0]
            return self._update_candidate(
                self.POINT,
                confidence,
                "Point · index finger controls cursor",
                now,
            )

        self._update_candidate(self.NONE, 0.0, "No active gesture", now)
        self.last_gesture = self.NONE
        self.details = "No active gesture"
        return self.NONE

    @property
    def candidate_gesture(self):
        if (
            self._candidate_gesture != self.NONE
            and self._candidate_frames < self.stability_frames
        ):
            return self._candidate_gesture
        if (
            self._candidate_gesture == self.FIST
            and self._candidate_started_at is not None
            and self._candidate_elapsed < self.fist_hold_duration
        ):
            return self.FIST
        return self.NONE

    def reset_tracking(self):
        self._candidate_gesture = self.NONE
        self._candidate_frames = 0
        self._candidate_started_at = None
        self._candidate_elapsed = 0.0
        self._non_fist_frames = 0
        self.is_pinching = False
        self.last_gesture = self.NONE
        self.confidence = 0.0
        self.details = "Show your hand to the camera"
        self.finger_states = {}

    def reset(self):
        self.reset_tracking()
        self._fist_latched = False
