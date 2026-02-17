"""Core behavior tests."""

from __future__ import annotations

from datetime import datetime
import unittest

from autoclicker.core.config import AutoClickerConfig, TimeWindowSettings, is_inside_time_window
from autoclicker.core.keyboard_sender import KeyAction


class CoreTests(unittest.TestCase):
    def test_mouse_action_single_is_valid(self) -> None:
        action = KeyAction.parse("mouse_left")
        self.assertEqual(action.tokens, ["mouse_left"])

    def test_mouse_action_double_click_is_valid(self) -> None:
        action = KeyAction.parse("mouse_left_double")
        self.assertEqual(action.tokens, ["mouse_left_double"])

    def test_mouse_action_scroll_is_valid(self) -> None:
        action = KeyAction.parse("mouse_scroll_down")
        self.assertEqual(action.tokens, ["mouse_scroll_down"])

    def test_mouse_action_mixed_with_keyboard_is_invalid(self) -> None:
        with self.assertRaises(ValueError):
            KeyAction.parse("mouse_left+ctrl")

    def test_config_validation_rejects_unknown_key(self) -> None:
        config = AutoClickerConfig(key_combo="invalid_long_key_name")
        with self.assertRaises(ValueError):
            config.validate()

    def test_time_window_same_start_end_is_always_on(self) -> None:
        settings = TimeWindowSettings(enabled=True, start_time="09:00", end_time="09:00")
        now = datetime.strptime("22:15", "%H:%M")
        self.assertTrue(is_inside_time_window(now, settings))

    def test_scroll_steps_validation(self) -> None:
        config = AutoClickerConfig(key_combo="mouse_scroll_up", mouse_scroll_steps=0)
        with self.assertRaises(ValueError):
            config.validate()


if __name__ == "__main__":
    unittest.main()
