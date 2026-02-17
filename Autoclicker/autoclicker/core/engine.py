"""Execution engine shared by CLI and GUI."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import threading
import time
from typing import Callable

from .config import AutoClickerConfig, is_inside_time_window
from .keyboard_sender import KeyAction, KeyboardSender
from .randomizer import humanized_interval


EventCallback = Callable[["EngineEvent"], None]


@dataclass(slots=True)
class EngineEvent:
    name: str
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    payload: dict | None = None


class AutoClickerEngine:
    """Thread-based scheduler with pause/resume/stop control."""

    def __init__(
        self,
        config: AutoClickerConfig,
        sender: KeyboardSender | None = None,
        on_event: EventCallback | None = None,
    ) -> None:
        self.config = config
        self.config.validate()
        self._on_event = on_event
        self._sender = sender or KeyboardSender(dry_run=config.dry_run)
        self._action = KeyAction.parse(config.key_combo)

        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._thread: threading.Thread | None = None
        self.sent_count = 0

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            raise RuntimeError("Il motore e gia in esecuzione.")
        self._stop_event.clear()
        self._pause_event.clear()
        self.sent_count = 0
        self._emit("started", "Esecuzione avviata.")
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def pause(self) -> None:
        if not self._pause_event.is_set():
            self._pause_event.set()
            self._emit("paused", "Esecuzione in pausa.")

    def resume(self) -> None:
        if self._pause_event.is_set():
            self._pause_event.clear()
            self._emit("resumed", "Esecuzione ripresa.")

    def stop(self) -> None:
        if self._stop_event.is_set():
            return
        self._stop_event.set()
        self._pause_event.clear()
        self._emit("stopped", "Esecuzione fermata.")

    def wait(self, timeout: float | None = None) -> None:
        if self._thread:
            self._thread.join(timeout=timeout)

    def is_running(self) -> bool:
        return bool(self._thread and self._thread.is_alive() and not self._stop_event.is_set())

    def _run(self) -> None:
        try:
            if self.config.initial_delay.enabled and self.config.initial_delay.seconds > 0:
                self._emit(
                    "initial_delay",
                    f"Delay iniziale di {self.config.initial_delay.seconds:.2f} secondi.",
                )
                if not self._interruptible_sleep(self.config.initial_delay.seconds):
                    return

            while not self._stop_event.is_set():
                if self._pause_event.is_set():
                    time.sleep(0.2)
                    continue

                now = datetime.now()
                if not is_inside_time_window(now, self.config.time_window):
                    self._emit("waiting_window", "Fuori dalla finestra oraria, in attesa.")
                    time.sleep(1.0)
                    continue

                if self.config.repeat.enabled and self.sent_count >= self.config.repeat.count:
                    self._emit("completed", "Numero massimo di esecuzioni raggiunto.")
                    self._stop_event.set()
                    break

                sleep_for = humanized_interval(self.config.interval_seconds, self.config.randomization)
                self._emit(
                    "scheduled",
                    f"Prossima pressione tra {sleep_for:.2f} secondi.",
                    payload={"next_in_seconds": sleep_for},
                )
                if not self._interruptible_sleep(sleep_for):
                    return

                self._sender.trigger(
                    self._action,
                    combo_key_delay_ms=self.config.combo_key_delay_ms,
                    mouse_scroll_steps=self.config.mouse_scroll_steps,
                )
                self.sent_count += 1
                self._emit(
                    "triggered",
                    f"Tasto/combinazione inviata ({self.sent_count}).",
                    payload={"sent_count": self.sent_count},
                )
        except Exception as exc:
            self._stop_event.set()
            self._emit("error", f"Errore runtime: {exc}")
        finally:
            self._emit("thread_exit", "Thread terminato.")

    def _interruptible_sleep(self, duration_s: float) -> bool:
        remaining = duration_s
        while remaining > 0:
            if self._stop_event.is_set():
                return False
            if self._pause_event.is_set():
                time.sleep(0.2)
                continue
            step = min(0.2, remaining)
            time.sleep(step)
            remaining -= step
        return True

    def _emit(self, name: str, message: str, payload: dict | None = None) -> None:
        if self._on_event is None:
            return
        self._on_event(EngineEvent(name=name, message=message, payload=payload))
