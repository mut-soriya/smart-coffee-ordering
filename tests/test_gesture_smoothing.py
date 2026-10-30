import unittest
from types import SimpleNamespace

from src.cursor_controller import CursorController
from src.gesture_engine import GestureEngine


def make_hand(wrist_x=0.5, pinch_distance=0.3):
    hand = [SimpleNamespace(x=0.5, y=0.5) for _ in range(21)]
    hand[0] = SimpleNamespace(x=wrist_x, y=0.9)
    for offset, x in enumerate((0.35, 0.45, 0.55, 0.65)):
        mcp = 5 + offset * 4
        hand[mcp] = SimpleNamespace(x=x, y=0.65)
        hand[mcp + 1] = SimpleNamespace(x=x, y=0.68)
        hand[mcp + 2] = SimpleNamespace(x=x, y=0.72)
        hand[mcp + 3] = SimpleNamespace(x=x, y=0.75)
    hand[9] = SimpleNamespace(x=0.45, y=0.65)
    hand[4] = SimpleNamespace(x=0.45, y=0.65)
    hand[8] = SimpleNamespace(x=0.5 + pinch_distance, y=0.4)
    if pinch_distance < 0.2:
        hand[4] = SimpleNamespace(x=0.5, y=0.4)
        hand[8] = SimpleNamespace(x=0.5 + pinch_distance, y=0.4)
    return hand


def make_open_hand():
    hand = make_hand()
    for offset, x in enumerate((0.35, 0.45, 0.55, 0.65)):
        mcp = 5 + offset * 4
        hand[mcp] = SimpleNamespace(x=x, y=0.65)
        hand[mcp + 1] = SimpleNamespace(x=x, y=0.52)
        hand[mcp + 2] = SimpleNamespace(x=x, y=0.40)
        hand[mcp + 3] = SimpleNamespace(x=x, y=0.28)
    return hand


def make_two_finger_hand():
    hand = make_hand()
    open_hand = make_open_hand()
    for index in range(5, 13):
        hand[index] = open_hand[index]
    return hand


def make_relax_hand():
    hand = make_open_hand()
    curled_hand = make_hand()
    for index in range(17, 21):
        hand[index] = curled_hand[index]
    return hand


def make_fist_hand():
    hand = make_hand()
    for offset, x in enumerate((0.35, 0.45, 0.55, 0.65)):
        mcp = 5 + offset * 4
        hand[mcp + 2] = SimpleNamespace(x=x, y=0.65)
        hand[mcp + 3] = SimpleNamespace(x=x, y=0.62)
    return hand


class CursorControllerTests(unittest.TestCase):
    def test_cursor_smoothly_tracks_and_clamps_fingertip(self):
        cursor = CursorController(
            screen_width=1000,
            screen_height=500,
            margin=0.1,
        )
        start_hand = make_hand()
        start_hand[8] = SimpleNamespace(x=0.5, y=0.5)
        hand = make_hand()
        hand[8] = SimpleNamespace(x=0.9, y=0.9)

        cursor.update(start_hand, timestamp=1.0)
        first_x, first_y = cursor.update(hand, timestamp=1.033)
        self.assertGreater(first_x, 500)
        self.assertGreater(first_y, 250)
        self.assertLess(first_x, 1000)
        self.assertLess(first_y, 500)

        for frame in range(2, 80):
            final_x, final_y = cursor.update(hand, timestamp=1 + frame / 30)

        self.assertEqual(final_x, 1000)
        self.assertEqual(final_y, 500)

    def test_small_landmark_jitter_stays_inside_dead_zone(self):
        cursor = CursorController(
            screen_width=1000,
            screen_height=500,
        )
        hand = make_hand()
        hand[8] = SimpleNamespace(x=0.5, y=0.5)
        cursor.update(hand, timestamp=1.0)
        before = cursor.get_position()
        hand[8] = SimpleNamespace(x=0.501, y=0.501)

        self.assertEqual(cursor.update(hand, timestamp=1.033), before)

    def test_cursor_can_track_two_finger_midpoint(self):
        cursor = CursorController(
            screen_width=1000,
            screen_height=500,
            margin=0.1,
        )

        self.assertEqual(cursor.update_point(0.5, 0.5, timestamp=1.0), (500, 250))
        first_x, first_y = cursor.update_point(0.9, 0.9, timestamp=1.033)
        self.assertGreater(first_x, 500)
        self.assertGreater(first_y, 250)
        self.assertLess(first_x, 1000)
        self.assertLess(first_y, 500)


class GestureEngineTests(unittest.TestCase):
    def test_pinch_requires_stability_and_uses_release_hysteresis(self):
        engine = GestureEngine()

        self.assertEqual(engine.detect(make_hand(pinch_distance=0.04)), "NONE")
        self.assertEqual(engine.detect(make_hand(pinch_distance=0.04)), "PINCH")
        self.assertEqual(engine.detect(make_hand(pinch_distance=0.07)), "PINCH")
        self.assertEqual(engine.detect(make_hand(pinch_distance=0.30)), "NONE")

    def test_reset_clears_pinch_state(self):
        engine = GestureEngine()
        engine.detect(make_hand(pinch_distance=0.04))
        engine.detect(make_hand(pinch_distance=0.04))
        engine.reset()

        self.assertEqual(engine.detect(make_hand(pinch_distance=0.04)), "NONE")

    def test_pinch_threshold_adapts_to_hand_scale(self):
        small_hand = make_hand(pinch_distance=0.05)
        large_hand = make_hand(pinch_distance=0.10)
        small_hand[9] = SimpleNamespace(x=0.45, y=0.65)
        large_hand[9] = SimpleNamespace(x=0.5, y=0.5)
        engine = GestureEngine()

        self.assertEqual(engine.detect(small_hand), "NONE")
        self.assertEqual(engine.detect(small_hand), "PINCH")
        engine.reset()
        self.assertEqual(engine.detect(large_hand), "NONE")
        self.assertEqual(engine.detect(large_hand), "PINCH")

    def test_open_hand_has_no_active_gesture(self):
        engine = GestureEngine()
        hand = make_open_hand()

        self.assertEqual(engine.detect(hand), "NONE")
        self.assertEqual(engine.detect(hand), "NONE")

    def test_one_index_finger_is_enough_to_point(self):
        engine = GestureEngine()
        hand = make_hand()

        engine.detect(hand)
        result = engine.detect(hand)

        self.assertEqual(result, "POINT")
        self.assertEqual(engine.last_gesture, "POINT")
        self.assertIn("index finger", engine.details)
        self.assertGreater(engine.confidence, 0.7)

    def test_pointing_tolerates_a_bent_index_finger(self):
        engine = GestureEngine()
        hand = make_hand()
        hand[7] = SimpleNamespace(x=0.37, y=0.695)

        self.assertEqual(engine.detect(hand), "NONE")
        self.assertEqual(engine.detect(hand), "POINT")

    def test_two_finger_scroll_requires_stable_index_and_middle_fingers(self):
        engine = GestureEngine()
        hand = make_two_finger_hand()

        self.assertEqual(engine.detect(hand), "NONE")
        self.assertEqual(engine.detect(hand), "TWO_FINGER_SCROLL")
        self.assertIn("index and middle", engine.details)

    def test_three_fingers_signal_relax_after_stability(self):
        engine = GestureEngine()
        hand = make_relax_hand()

        self.assertEqual(engine.detect(hand), "NONE")
        self.assertEqual(engine.detect(hand), "RELAX")
        self.assertIn("hold-to-select paused", engine.details)

    def test_pinch_takes_priority_over_scroll_candidate(self):
        engine = GestureEngine()
        hand = make_two_finger_hand()
        hand[4] = hand[8]

        self.assertEqual(engine.detect(hand), "NONE")
        self.assertEqual(engine.candidate_gesture, "PINCH")
        self.assertEqual(engine.detect(hand), "PINCH")

    def test_fist_requires_a_stable_400ms_hold(self):
        engine = GestureEngine()
        hand = make_fist_hand()

        self.assertEqual(engine.detect(hand, timestamp=1.0), "NONE")
        self.assertEqual(engine.detect(hand, timestamp=1.2), "NONE")
        self.assertEqual(engine.detect(hand, timestamp=1.39), "NONE")
        self.assertEqual(engine.detect(hand, timestamp=1.41), "FIST")
        self.assertIn("fingers curled", engine.details)

    def test_fist_does_not_repeat_until_hand_releases(self):
        engine = GestureEngine()
        fist = make_fist_hand()
        open_hand = make_open_hand()

        self.assertEqual(engine.detect(fist, timestamp=1.0), "NONE")
        self.assertEqual(engine.detect(fist, timestamp=1.2), "NONE")
        self.assertEqual(engine.detect(fist, timestamp=1.41), "FIST")
        engine.detect(None, timestamp=1.5)

        self.assertEqual(engine.detect(fist, timestamp=2.0), "NONE")
        self.assertEqual(engine.detect(fist, timestamp=2.2), "NONE")
        self.assertEqual(engine.detect(fist, timestamp=2.41), "NONE")
        self.assertEqual(engine.detect(open_hand, timestamp=2.5), "NONE")
        self.assertEqual(engine.detect(open_hand, timestamp=2.6), "NONE")
        self.assertEqual(engine.detect(fist, timestamp=3.0), "NONE")
        self.assertEqual(engine.detect(fist, timestamp=3.2), "NONE")
    def test_realistic_fist_is_not_misidentified_as_pinch(self):
        # Even when thumb tip is near the curled index finger, a fist is detected as FIST, not PINCH
        hand = make_fist_hand()
        hand[4] = SimpleNamespace(x=hand[8].x, y=hand[8].y)  # Thumb touching curled index tip
        engine = GestureEngine()

        self.assertEqual(engine.detect(hand, timestamp=1.0), "NONE")
        self.assertEqual(engine.detect(hand, timestamp=1.2), "NONE")
        self.assertEqual(engine.detect(hand, timestamp=1.41), "FIST")


if __name__ == "__main__":
    unittest.main()
