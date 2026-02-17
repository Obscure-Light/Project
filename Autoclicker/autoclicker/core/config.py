"""Configuration models and validation helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
from pathlib import Path
from typing import Any

from .randomizer import RandomizationSettings


@dataclass(slots=True)
class TimeWindowSettings:
    enabled: bool = False
    start_time: str = "09:00"
    end_time: str = "18:00"


@dataclass(slots=True)
class RepeatSettings:
    enabled: bool = False
    count: int = 1


@dataclass(slots=True)
class DelaySettings:
    enabled: bool = False
    seconds: float = 0.0


@dataclass(slots=True)
class AutoClickerConfig:
    """Serializable configuration used by both CLI and GUI."""

    key_combo: str = "numlock"
    interval_seconds: float = 300.0
    combo_key_delay_ms: int = 60
    mouse_scroll_steps: int = 1
    randomization: RandomizationSettings = field(default_factory=RandomizationSettings)
    time_window: TimeWindowSettings = field(default_factory=TimeWindowSettings)
    repeat: RepeatSettings = field(default_factory=RepeatSettings)
    initial_delay: DelaySettings = field(default_factory=DelaySettings)
    dry_run: bool = False

    def validate(self) -> None:
        from .keyboard_sender import KeyAction

        if self.interval_seconds <= 0:
            raise ValueError("L'intervallo deve essere maggiore di 0.")
        if self.combo_key_delay_ms < 0:
            raise ValueError("Il delay tra tasti deve essere >= 0.")
        if self.mouse_scroll_steps <= 0:
            raise ValueError("Gli step di scroll mouse devono essere > 0.")
        if self.repeat.enabled and self.repeat.count <= 0:
            raise ValueError("Il numero di ripetizioni deve essere maggiore di 0.")
        if self.initial_delay.enabled and self.initial_delay.seconds < 0:
            raise ValueError("Il delay iniziale deve essere >= 0.")

        if self.time_window.enabled:
            _parse_hhmm(self.time_window.start_time, "Ora inizio")
            _parse_hhmm(self.time_window.end_time, "Ora fine")

        if self.randomization.enabled:
            if self.randomization.stddev_percent < 0:
                raise ValueError("La deviazione standard percentuale deve essere >= 0.")
            if self.randomization.min_percent > self.randomization.max_percent:
                raise ValueError("Il range minimo random non puo superare il massimo.")

        # Validate supported keyboard/mouse action syntax early.
        KeyAction.parse(self.key_combo)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AutoClickerConfig":
        randomization = RandomizationSettings(**data.get("randomization", {}))
        time_window = TimeWindowSettings(**data.get("time_window", {}))
        repeat = RepeatSettings(**data.get("repeat", {}))
        initial_delay = DelaySettings(**data.get("initial_delay", {}))

        config = cls(
            key_combo=data.get("key_combo", "numlock"),
            interval_seconds=float(data.get("interval_seconds", 300.0)),
            combo_key_delay_ms=int(data.get("combo_key_delay_ms", 60)),
            mouse_scroll_steps=int(data.get("mouse_scroll_steps", 1)),
            randomization=randomization,
            time_window=time_window,
            repeat=repeat,
            initial_delay=initial_delay,
            dry_run=bool(data.get("dry_run", False)),
        )
        config.validate()
        return config

    @classmethod
    def load(cls, path: Path) -> "AutoClickerConfig":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_dict(data)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")


def _parse_hhmm(value: str, field_name: str) -> datetime:
    try:
        return datetime.strptime(value, "%H:%M")
    except ValueError as exc:
        raise ValueError(f"{field_name} non valida. Formato richiesto HH:MM.") from exc


def is_inside_time_window(now: datetime, settings: TimeWindowSettings) -> bool:
    """Evaluate if current local time is inside the configured window."""
    if not settings.enabled:
        return True

    start = _parse_hhmm(settings.start_time, "Ora inizio").time()
    end = _parse_hhmm(settings.end_time, "Ora fine").time()
    current = now.time()

    # Same start/end means "always on" for user convenience.
    if start == end:
        return True

    # Supports windows that cross midnight, e.g. 22:00 -> 06:00.
    if start <= end:
        return start <= current <= end
    return current >= start or current <= end
