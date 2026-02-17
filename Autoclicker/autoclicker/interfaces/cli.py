"""CLI interface for Autoclicker."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import signal
import time

from autoclicker.core.config import AutoClickerConfig
from autoclicker.core.engine import AutoClickerEngine, EngineEvent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Autoclicker CLI")
    parser.add_argument("--config", type=Path, help="Carica configurazione da file JSON.")
    parser.add_argument("--save-config", type=Path, help="Salva la configurazione finale in JSON.")

    parser.add_argument(
        "--key",
        help=(
            "Azione input: tasto/combo (numlock, ctrl+shift+x), "
            "click (mouse_left, mouse_left_double) o scroll (mouse_scroll_up/down)."
        ),
    )
    parser.add_argument("--interval", type=float, help="Intervallo base in secondi.")
    parser.add_argument("--combo-delay-ms", type=int, help="Delay tra tasti della combinazione.")
    parser.add_argument("--mouse-scroll-steps", type=int, help="Step per azioni scroll mouse.")

    parser.add_argument("--randomization", choices=["on", "off"])
    parser.add_argument("--random-stddev", type=float, help="Deviazione standard %%.")
    parser.add_argument("--random-min", type=float, help="Delta minimo %%.")
    parser.add_argument("--random-max", type=float, help="Delta massimo %%.")

    parser.add_argument("--time-window", choices=["on", "off"])
    parser.add_argument("--start-time", help="Ora inizio HH:MM.")
    parser.add_argument("--end-time", help="Ora fine HH:MM.")

    parser.add_argument("--repeat", choices=["on", "off"])
    parser.add_argument("--repeat-count", type=int)

    parser.add_argument("--initial-delay", choices=["on", "off"])
    parser.add_argument("--initial-delay-seconds", type=float)

    parser.add_argument("--dry-run", action="store_true", help="Simula senza inviare tasti reali.")
    return parser


def run_cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        config = _build_config(args)
    except Exception as exc:
        print(f"[ERRORE] Configurazione non valida: {exc}")
        return 2

    if args.save_config:
        config.save(args.save_config)
        print(f"[INFO] Config salvata in: {args.save_config}")

    try:
        engine = AutoClickerEngine(config=config, on_event=_print_event)
    except Exception as exc:
        print(f"[ERRORE] Impossibile avviare il motore: {exc}")
        return 2

    def _graceful_stop(_signum: int, _frame: object) -> None:
        print("\n[INFO] Ricevuto stop, chiusura in corso...")
        engine.stop()

    signal.signal(signal.SIGINT, _graceful_stop)

    try:
        engine.start()
    except Exception as exc:
        print(f"[ERRORE] Avvio fallito: {exc}")
        return 2
    try:
        while engine.is_running():
            time.sleep(0.2)
    finally:
        engine.stop()
        engine.wait(timeout=2.0)
    return 0


def _build_config(args: argparse.Namespace) -> AutoClickerConfig:
    if args.config:
        if not args.config.exists():
            raise FileNotFoundError(f"File config non trovato: {args.config}")
        config = AutoClickerConfig.load(args.config)
    else:
        config = AutoClickerConfig()

    if args.key is not None:
        config.key_combo = args.key
    if args.interval is not None:
        config.interval_seconds = args.interval
    if args.combo_delay_ms is not None:
        config.combo_key_delay_ms = args.combo_delay_ms
    if args.mouse_scroll_steps is not None:
        config.mouse_scroll_steps = args.mouse_scroll_steps
    if args.randomization is not None:
        config.randomization.enabled = args.randomization == "on"
    if args.random_stddev is not None:
        config.randomization.stddev_percent = args.random_stddev
    if args.random_min is not None:
        config.randomization.min_percent = args.random_min
    if args.random_max is not None:
        config.randomization.max_percent = args.random_max
    if args.time_window is not None:
        config.time_window.enabled = args.time_window == "on"
    if args.start_time is not None:
        config.time_window.start_time = args.start_time
    if args.end_time is not None:
        config.time_window.end_time = args.end_time
    if args.repeat is not None:
        config.repeat.enabled = args.repeat == "on"
    if args.repeat_count is not None:
        config.repeat.count = args.repeat_count
    if args.initial_delay is not None:
        config.initial_delay.enabled = args.initial_delay == "on"
    if args.initial_delay_seconds is not None:
        config.initial_delay.seconds = args.initial_delay_seconds
    if args.dry_run:
        config.dry_run = True
    config.validate()
    return config


def _print_event(event: EngineEvent) -> None:
    ts = event.timestamp.strftime("%H:%M:%S")
    print(f"[{ts}] {event.name.upper()}: {event.message}")
    if event.payload:
        print(f"  payload={event.payload}")
