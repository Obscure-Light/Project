"""CLI behavior tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from autoclicker.interfaces.cli import _build_config, build_parser


class CliTests(unittest.TestCase):
    def test_config_file_values_are_preserved_when_no_overrides(self) -> None:
        parser = build_parser()
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "profile.json"
            path.write_text(
                json.dumps(
                    {
                        "key_combo": "mouse_right",
                        "interval_seconds": 2.5,
                        "repeat": {"enabled": True, "count": 3},
                    }
                ),
                encoding="utf-8",
            )
            args = parser.parse_args(["--config", str(path)])
            cfg = _build_config(args)
            self.assertEqual(cfg.key_combo, "mouse_right")
            self.assertEqual(cfg.interval_seconds, 2.5)
            self.assertTrue(cfg.repeat.enabled)
            self.assertEqual(cfg.repeat.count, 3)

    def test_cli_values_override_config_file(self) -> None:
        parser = build_parser()
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "profile.json"
            path.write_text(
                json.dumps({"key_combo": "numlock", "interval_seconds": 3.0}),
                encoding="utf-8",
            )
            args = parser.parse_args(["--config", str(path), "--interval", "9"])
            cfg = _build_config(args)
            self.assertEqual(cfg.key_combo, "numlock")
            self.assertEqual(cfg.interval_seconds, 9.0)

    def test_cli_scroll_steps_override(self) -> None:
        parser = build_parser()
        args = parser.parse_args(["--key", "mouse_scroll_up", "--mouse-scroll-steps", "4"])
        cfg = _build_config(args)
        self.assertEqual(cfg.key_combo, "mouse_scroll_up")
        self.assertEqual(cfg.mouse_scroll_steps, 4)


if __name__ == "__main__":
    unittest.main()
