"""Application entrypoint.

Default behavior:
- no args: launch GUI
- args present: run CLI
"""

from __future__ import annotations

import sys


def main() -> int:
    if len(sys.argv) > 1:
        from autoclicker.interfaces.cli import run_cli

        return run_cli(sys.argv[1:])
    from autoclicker.interfaces.gui import run_gui

    return run_gui()


if __name__ == "__main__":
    raise SystemExit(main())
