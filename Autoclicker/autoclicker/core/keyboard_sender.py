"""Keyboard sending utilities backed by pynput."""

from __future__ import annotations

from dataclasses import dataclass
import time

SPECIAL_KEY_NAMES = {
    "alt",
    "alt_l",
    "alt_r",
    "backspace",
    "capslock",
    "ctrl",
    "ctrl_l",
    "ctrl_r",
    "delete",
    "down",
    "end",
    "enter",
    "esc",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
    "f11",
    "f12",
    "home",
    "insert",
    "left",
    "numlock",
    "pagedown",
    "pageup",
    "right",
    "shift",
    "shift_l",
    "shift_r",
    "space",
    "tab",
    "up",
}

MOUSE_BUTTON_NAMES = {"mouse_left", "mouse_right", "mouse_middle"}
MOUSE_DOUBLE_BUTTON_NAMES = {
    "mouse_left_double",
    "mouse_right_double",
    "mouse_middle_double",
}
MOUSE_SCROLL_NAMES = {"mouse_scroll_up", "mouse_scroll_down"}
MOUSE_ACTION_NAMES = MOUSE_BUTTON_NAMES | MOUSE_DOUBLE_BUTTON_NAMES | MOUSE_SCROLL_NAMES


def _special_keys() -> dict[str, object]:
    from pynput.keyboard import Key

    return {
        "alt": Key.alt,
        "alt_l": Key.alt_l,
        "alt_r": Key.alt_r,
        "backspace": Key.backspace,
        "capslock": Key.caps_lock,
        "ctrl": Key.ctrl,
        "ctrl_l": Key.ctrl_l,
        "ctrl_r": Key.ctrl_r,
        "delete": Key.delete,
        "down": Key.down,
        "end": Key.end,
        "enter": Key.enter,
        "esc": Key.esc,
        "f1": Key.f1,
        "f2": Key.f2,
        "f3": Key.f3,
        "f4": Key.f4,
        "f5": Key.f5,
        "f6": Key.f6,
        "f7": Key.f7,
        "f8": Key.f8,
        "f9": Key.f9,
        "f10": Key.f10,
        "f11": Key.f11,
        "f12": Key.f12,
        "home": Key.home,
        "insert": Key.insert,
        "left": Key.left,
        "numlock": Key.num_lock,
        "pagedown": Key.page_down,
        "pageup": Key.page_up,
        "right": Key.right,
        "shift": Key.shift,
        "shift_l": Key.shift_l,
        "shift_r": Key.shift_r,
        "space": Key.space,
        "tab": Key.tab,
        "up": Key.up,
    }

def _mouse_buttons() -> dict[str, object]:
    from pynput.mouse import Button

    return {
        "mouse_left": Button.left,
        "mouse_right": Button.right,
        "mouse_middle": Button.middle,
        "mouse_left_double": Button.left,
        "mouse_right_double": Button.right,
        "mouse_middle_double": Button.middle,
    }


@dataclass(slots=True)
class KeyAction:
    tokens: list[str]

    @classmethod
    def parse(cls, expression: str) -> "KeyAction":
        tokens: list[str] = []
        for raw in expression.split("+"):
            token = raw.strip().lower()
            if not token:
                continue
            if token in SPECIAL_KEY_NAMES or token in MOUSE_ACTION_NAMES:
                tokens.append(token)
                continue
            if len(token) == 1:
                tokens.append(token)
                continue
            raise ValueError(f"Tasto non supportato: '{raw}'.")

        if not tokens:
            raise ValueError("Specifica almeno un tasto o combinazione.")

        mouse_tokens = [token for token in tokens if token in MOUSE_ACTION_NAMES]
        if mouse_tokens and len(tokens) > 1:
            raise ValueError("Le azioni mouse supportano solo azione singola senza combinazioni.")
        return cls(tokens=tokens)


class KeyboardSender:
    """Sends a single key or a multi-key combination."""

    def __init__(self, dry_run: bool = False) -> None:
        self._dry_run = dry_run
        if self._dry_run:
            self._controller = None
            self._mouse = None
            self._special_keys = {}
            self._mouse_buttons = {}
            return
        try:
            from pynput.keyboard import Controller
            from pynput.mouse import Controller as MouseController
        except ImportError as exc:
            raise RuntimeError(
                "Dipendenza mancante: installa requirements.txt prima di avviare il tool."
            ) from exc
        self._controller = Controller()
        self._mouse = MouseController()
        self._special_keys = _special_keys()
        self._mouse_buttons = _mouse_buttons()

    def trigger(self, action: KeyAction, combo_key_delay_ms: int, mouse_scroll_steps: int = 1) -> None:
        if self._dry_run:
            return

        if len(action.tokens) == 1:
            token_name = action.tokens[0]
            if token_name in MOUSE_BUTTON_NAMES:
                self._mouse.click(self._mouse_buttons[token_name], 1)
                return
            if token_name in MOUSE_DOUBLE_BUTTON_NAMES:
                self._mouse.click(self._mouse_buttons[token_name], 2)
                return
            if token_name == "mouse_scroll_up":
                self._mouse.scroll(0, mouse_scroll_steps)
                return
            if token_name == "mouse_scroll_down":
                self._mouse.scroll(0, -mouse_scroll_steps)
                return
            token = self._resolve_keyboard_token(token_name)
            self._controller.press(token)
            self._controller.release(token)
            return

        delay_s = combo_key_delay_ms / 1000.0
        pressed: list[object] = []
        # Press keys in order, release in reverse order for realistic combos.
        for token_name in action.tokens:
            token = self._resolve_keyboard_token(token_name)
            self._controller.press(token)
            pressed.append(token)
            if delay_s > 0:
                time.sleep(delay_s)

        for token in reversed(pressed):
            self._controller.release(token)
            if delay_s > 0:
                time.sleep(delay_s)

    def _resolve_keyboard_token(self, token_name: str) -> object:
        return self._special_keys.get(token_name, token_name)
