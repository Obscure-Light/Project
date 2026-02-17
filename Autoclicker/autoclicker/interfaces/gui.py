"""Italian GUI built with customtkinter."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import queue
import tkinter.messagebox as mbox

import customtkinter as ctk

from autoclicker.core.config import AutoClickerConfig
from autoclicker.core.engine import AutoClickerEngine, EngineEvent
from autoclicker.core.keyboard_sender import KeyAction


KEYBOARD_LAYOUT: list[list[tuple[str, str]]] = [
    [("Esc", "esc"), ("F1", "f1"), ("F2", "f2"), ("F3", "f3"), ("F4", "f4"), ("F5", "f5"), ("F6", "f6"), ("F7", "f7"), ("F8", "f8"), ("F9", "f9"), ("F10", "f10"), ("F11", "f11"), ("F12", "f12")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("0", "0"), ("Tab", "tab"), ("Space", "space"), ("Enter", "enter")],
    [("Q", "q"), ("W", "w"), ("E", "e"), ("R", "r"), ("T", "t"), ("Y", "y"), ("U", "u"), ("I", "i"), ("O", "o"), ("P", "p"), ("Backspace", "backspace")],
    [("A", "a"), ("S", "s"), ("D", "d"), ("F", "f"), ("G", "g"), ("H", "h"), ("J", "j"), ("K", "k"), ("L", "l"), ("NumLock", "numlock"), ("Delete", "delete")],
    [("Z", "z"), ("X", "x"), ("C", "c"), ("V", "v"), ("B", "b"), ("N", "n"), ("M", "m"), ("Home", "home"), ("End", "end"), ("PgUp", "pageup"), ("PgDn", "pagedown")],
    [("Ctrl", "ctrl"), ("Shift", "shift"), ("Alt", "alt"), ("Up", "up"), ("Down", "down"), ("Left", "left"), ("Right", "right"), ("Insert", "insert")],
    [("Mouse Sinistro", "mouse_left"), ("Mouse Destro", "mouse_right"), ("Mouse Centrale", "mouse_middle")],
    [("Doppio SX", "mouse_left_double"), ("Doppio DX", "mouse_right_double"), ("Doppio Centrale", "mouse_middle_double")],
    [("Scroll Su", "mouse_scroll_up"), ("Scroll Giu", "mouse_scroll_down")],
]


class KeyboardPicker(ctk.CTkToplevel):
    """Popup keyboard to build a key/combo expression visually."""

    def __init__(self, master: ctk.CTk, initial_value: str) -> None:
        super().__init__(master=master)
        self.title("Selettore Tastiera")
        self.geometry("980x460")
        self.minsize(980, 460)
        self.transient(master)
        self.grab_set()

        self.result: str | None = None
        self._tokens: list[str] = [t.strip() for t in initial_value.split("+") if t.strip()]

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self,
            text="Clicca per comporre input tastiera o mouse. Formato esempio: 'ctrl+shift+x' oppure 'mouse_left'.",
            anchor="w",
            justify="left",
        ).grid(row=0, column=0, padx=14, pady=(12, 6), sticky="ew")

        self.combo_entry = ctk.CTkEntry(self, height=36)
        self.combo_entry.grid(row=1, column=0, padx=14, pady=6, sticky="ew")
        self._render_tokens()

        kb_frame = ctk.CTkScrollableFrame(self, label_text="Tastiera")
        kb_frame.grid(row=2, column=0, padx=14, pady=8, sticky="nsew")
        kb_frame.grid_columnconfigure(0, weight=1)

        row_index = 0
        for row_keys in KEYBOARD_LAYOUT:
            row_frame = ctk.CTkFrame(kb_frame)
            row_frame.grid(row=row_index, column=0, padx=6, pady=6, sticky="ew")
            for col_index, (label, token) in enumerate(row_keys):
                ctk.CTkButton(
                    row_frame,
                    text=label,
                    width=68,
                    command=lambda t=token: self._add_token(t),
                ).grid(row=0, column=col_index, padx=4, pady=4)
            row_index += 1

        controls = ctk.CTkFrame(self)
        controls.grid(row=3, column=0, padx=14, pady=(4, 12), sticky="ew")
        controls.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkButton(controls, text="Annulla", command=self._cancel).grid(row=0, column=0, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(controls, text="Cancella", command=self._clear).grid(row=0, column=1, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(controls, text="Indietro", command=self._pop).grid(row=0, column=2, padx=6, pady=8, sticky="ew")
        ctk.CTkButton(controls, text="Usa combinazione", command=self._apply).grid(row=0, column=3, padx=6, pady=8, sticky="ew")

    def _render_tokens(self) -> None:
        text = "+".join(self._tokens)
        self.combo_entry.delete(0, "end")
        self.combo_entry.insert(0, text)

    def _add_token(self, token: str) -> None:
        self._tokens.append(token)
        self._render_tokens()

    def _clear(self) -> None:
        self._tokens = []
        self._render_tokens()

    def _pop(self) -> None:
        if self._tokens:
            self._tokens.pop()
            self._render_tokens()

    def _cancel(self) -> None:
        self.result = None
        self.destroy()

    def _apply(self) -> None:
        value = self.combo_entry.get().strip().lower()
        if not value:
            mbox.showwarning("Tastiera", "Inserisci almeno un tasto.")
            return
        try:
            KeyAction.parse(value)
        except ValueError as exc:
            mbox.showwarning("Tastiera", str(exc))
            return
        self.result = value
        self.destroy()


class AutoClickerApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Autoclicker")
        self.geometry("1180x760")
        self.minsize(1080, 720)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._event_queue: queue.Queue[EngineEvent] = queue.Queue()
        self._engine: AutoClickerEngine | None = None

        self._build_ui()
        self.after(200, self._poll_events)

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        left_panel = ctk.CTkScrollableFrame(self, label_text="Configurazione")
        left_panel.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="nsew")
        left_panel.grid_columnconfigure(0, weight=1)

        self._build_action_section(left_panel)
        self._build_random_section(left_panel)
        self._build_time_section(left_panel)
        self._build_repeat_section(left_panel)
        self._build_startup_section(left_panel)
        self._build_misc_section(left_panel)
        self._build_buttons(left_panel)

        right_panel = ctk.CTkFrame(self)
        right_panel.grid(row=0, column=1, padx=(8, 16), pady=16, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        right_panel.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(right_panel, text="Stato Runtime", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, padx=12, pady=(12, 4), sticky="w"
        )
        self.status_label = ctk.CTkLabel(right_panel, text="Pronto", anchor="w")
        self.status_label.grid(row=1, column=0, padx=12, pady=(0, 8), sticky="ew")

        ctk.CTkLabel(
            right_panel,
            text="Dettagli: i campi con switch OFF non influenzano l'esecuzione.",
            anchor="w",
            justify="left",
            text_color="gray70",
        ).grid(row=2, column=0, padx=12, pady=(0, 8), sticky="ew")

        self.log_box = ctk.CTkTextbox(right_panel)
        self.log_box.grid(row=3, column=0, padx=12, pady=(0, 12), sticky="nsew")

    def _build_action_section(self, parent: ctk.CTkScrollableFrame) -> None:
        section = _section_frame(parent, "Azione Tasti")
        section.grid_columnconfigure(0, weight=1)

        self.key_entry = _entry_with_details(
            section,
            "Tasto / Combinazione / Mouse",
            "numlock",
            "Formato: tasto (numlock), combo (ctrl+shift+x), click (mouse_left_double) o scroll (mouse_scroll_up).",
            1,
            0,
        )
        ctk.CTkButton(section, text="Tastiera", command=self._open_keyboard_picker).grid(
            row=4, column=0, padx=8, pady=(4, 8), sticky="e"
        )

        self.interval_entry = _entry_with_details(
            section,
            "Intervallo base (secondi)",
            "300",
            "Tempo di attesa tra una pressione e la successiva.",
            5,
            0,
        )
        self.combo_delay_entry = _entry_with_details(
            section,
            "Delay tra tasti combo (ms)",
            "60",
            "Usato solo quando la combinazione ha piu tasti.",
            8,
            0,
        )
        self.mouse_scroll_steps_entry = _entry_with_details(
            section,
            "Step scroll mouse",
            "1",
            "Usato solo per mouse_scroll_up / mouse_scroll_down.",
            11,
            0,
        )

    def _build_random_section(self, parent: ctk.CTkScrollableFrame) -> None:
        section = _section_frame(parent, "Randomizzazione Umana")
        section.grid_columnconfigure(0, weight=1)

        self.random_switch = _switch_with_details(
            section,
            "Attiva randomizzazione",
            "ON: intervallo variabile su distribuzione gaussiana.",
            1,
            command=self._refresh_state_controls,
        )
        self.random_std_entry = _entry_with_details(section, "Deviazione std %", "5", "Intensita della variabilita.", 3, 0)
        self.random_min_entry = _entry_with_details(section, "Delta minimo %", "-10", "Limite inferiore hard.", 6, 0)
        self.random_max_entry = _entry_with_details(section, "Delta massimo %", "10", "Limite superiore hard.", 9, 0)

    def _build_time_section(self, parent: ctk.CTkScrollableFrame) -> None:
        section = _section_frame(parent, "Finestra Oraria")
        section.grid_columnconfigure(0, weight=1)

        self.window_switch = _switch_with_details(
            section,
            "Attiva fascia oraria",
            "Esempio: 22:00 -> 06:00 e supportato.",
            1,
            command=self._refresh_state_controls,
        )
        self.start_time_entry = _entry_with_details(section, "Ora inizio (HH:MM)", "09:00", "Inizio validita esecuzione.", 3, 0)
        self.end_time_entry = _entry_with_details(section, "Ora fine (HH:MM)", "18:00", "Fine validita esecuzione.", 6, 0)

    def _build_repeat_section(self, parent: ctk.CTkScrollableFrame) -> None:
        section = _section_frame(parent, "Ripetizioni")
        section.grid_columnconfigure(0, weight=1)

        self.repeat_switch = _switch_with_details(
            section,
            "Limita numero pressioni",
            "OFF: esecuzione continua finche non premi Stop.",
            1,
            command=self._refresh_state_controls,
        )
        self.repeat_count_entry = _entry_with_details(section, "Numero pressioni", "1", "Numero totale di trigger.", 3, 0)

    def _build_startup_section(self, parent: ctk.CTkScrollableFrame) -> None:
        section = _section_frame(parent, "Avvio")
        section.grid_columnconfigure(0, weight=1)

        self.delay_switch = _switch_with_details(
            section,
            "Attiva delay iniziale",
            "Attesa solo prima del primo trigger.",
            1,
            command=self._refresh_state_controls,
        )
        self.initial_delay_entry = _entry_with_details(section, "Secondi delay iniziale", "0", "Valore >= 0.", 3, 0)

    def _build_misc_section(self, parent: ctk.CTkScrollableFrame) -> None:
        section = _section_frame(parent, "Modalita")
        self.dry_run_switch = _switch_with_details(
            section,
            "Modalita test (dry-run)",
            "Simula eventi senza inviare tasti reali.",
            1,
        )

    def _build_buttons(self, parent: ctk.CTkScrollableFrame) -> None:
        section = _section_frame(parent, "Controlli")
        section.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkButton(section, text="Avvia", command=self._start, height=40).grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(section, text="Pausa", command=self._pause, height=40).grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(section, text="Riprendi", command=self._resume, height=40).grid(row=0, column=2, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(section, text="Stop", command=self._stop, fg_color="#b63636", hover_color="#972d2d", height=40).grid(
            row=1, column=0, padx=8, pady=8, sticky="ew"
        )
        ctk.CTkButton(section, text="Salva profilo", command=self._save_profile, height=40).grid(row=1, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(section, text="Carica profilo", command=self._load_profile, height=40).grid(row=1, column=2, padx=8, pady=8, sticky="ew")

        self._refresh_state_controls()

    def _open_keyboard_picker(self) -> None:
        popup = KeyboardPicker(self, self.key_entry.get().strip())
        self.wait_window(popup)
        if popup.result:
            _set_entry(self.key_entry, popup.result)

    def _refresh_state_controls(self) -> None:
        _set_entry_state(self.random_std_entry, bool(self.random_switch.get()))
        _set_entry_state(self.random_min_entry, bool(self.random_switch.get()))
        _set_entry_state(self.random_max_entry, bool(self.random_switch.get()))
        _set_entry_state(self.start_time_entry, bool(self.window_switch.get()))
        _set_entry_state(self.end_time_entry, bool(self.window_switch.get()))
        _set_entry_state(self.repeat_count_entry, bool(self.repeat_switch.get()))
        _set_entry_state(self.initial_delay_entry, bool(self.delay_switch.get()))

    def _collect_config(self) -> AutoClickerConfig:
        config = AutoClickerConfig()
        config.key_combo = self.key_entry.get().strip()
        config.interval_seconds = float(self.interval_entry.get().strip())
        config.combo_key_delay_ms = int(self.combo_delay_entry.get().strip())
        config.mouse_scroll_steps = int(self.mouse_scroll_steps_entry.get().strip())
        config.randomization.enabled = bool(self.random_switch.get())
        config.randomization.stddev_percent = float(self.random_std_entry.get().strip())
        config.randomization.min_percent = float(self.random_min_entry.get().strip())
        config.randomization.max_percent = float(self.random_max_entry.get().strip())
        config.time_window.enabled = bool(self.window_switch.get())
        config.time_window.start_time = self.start_time_entry.get().strip()
        config.time_window.end_time = self.end_time_entry.get().strip()
        config.repeat.enabled = bool(self.repeat_switch.get())
        config.repeat.count = int(self.repeat_count_entry.get().strip())
        config.initial_delay.enabled = bool(self.delay_switch.get())
        config.initial_delay.seconds = float(self.initial_delay_entry.get().strip())
        config.dry_run = bool(self.dry_run_switch.get())
        config.validate()
        return config

    def _start(self) -> None:
        try:
            config = self._collect_config()
        except Exception as exc:
            mbox.showerror("Errore configurazione", str(exc))
            return

        if self._engine and self._engine.is_running():
            mbox.showwarning("Autoclicker", "Il motore e gia in esecuzione.")
            return

        try:
            self._engine = AutoClickerEngine(config=config, on_event=self._event_queue.put)
            self._engine.start()
            self._append_log("INFO", "Motore avviato.")
        except Exception as exc:
            mbox.showerror("Errore avvio", str(exc))

    def _pause(self) -> None:
        if self._engine:
            self._engine.pause()

    def _resume(self) -> None:
        if self._engine:
            self._engine.resume()

    def _stop(self) -> None:
        if self._engine:
            self._engine.stop()
            self._append_log("INFO", "Stop richiesto.")

    def _save_profile(self) -> None:
        try:
            config = self._collect_config()
            path = Path("autoclicker_profile.json")
            config.save(path)
            self._append_log("INFO", f"Profilo salvato in {path}.")
        except Exception as exc:
            mbox.showerror("Errore salvataggio", str(exc))

    def _load_profile(self) -> None:
        path = Path("autoclicker_profile.json")
        if not path.exists():
            mbox.showwarning("Profilo", "Nessun profilo trovato (autoclicker_profile.json).")
            return
        try:
            config = AutoClickerConfig.load(path)
            self._apply_config(config)
            self._append_log("INFO", f"Profilo caricato da {path}.")
        except Exception as exc:
            mbox.showerror("Errore caricamento", str(exc))

    def _apply_config(self, config: AutoClickerConfig) -> None:
        _set_entry(self.key_entry, config.key_combo)
        _set_entry(self.interval_entry, str(config.interval_seconds))
        _set_entry(self.combo_delay_entry, str(config.combo_key_delay_ms))
        _set_entry(self.mouse_scroll_steps_entry, str(config.mouse_scroll_steps))
        _set_switch(self.random_switch, config.randomization.enabled)
        _set_entry(self.random_std_entry, str(config.randomization.stddev_percent))
        _set_entry(self.random_min_entry, str(config.randomization.min_percent))
        _set_entry(self.random_max_entry, str(config.randomization.max_percent))
        _set_switch(self.window_switch, config.time_window.enabled)
        _set_entry(self.start_time_entry, config.time_window.start_time)
        _set_entry(self.end_time_entry, config.time_window.end_time)
        _set_switch(self.repeat_switch, config.repeat.enabled)
        _set_entry(self.repeat_count_entry, str(config.repeat.count))
        _set_switch(self.delay_switch, config.initial_delay.enabled)
        _set_entry(self.initial_delay_entry, str(config.initial_delay.seconds))
        _set_switch(self.dry_run_switch, config.dry_run)
        self._refresh_state_controls()

    def _poll_events(self) -> None:
        while True:
            try:
                event = self._event_queue.get_nowait()
            except queue.Empty:
                break
            sent = ""
            if event.payload and "sent_count" in event.payload:
                sent = f" | Inviati: {event.payload['sent_count']}"
            self.status_label.configure(text=f"{event.name.upper()}: {event.message}{sent}")
            self._append_log(event.name.upper(), event.message)
        self.after(200, self._poll_events)

    def _append_log(self, level: str, message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {level}: {message}\n")
        self.log_box.see("end")


def _section_frame(parent: ctk.CTkBaseClass, title: str) -> ctk.CTkFrame:
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="x", padx=6, pady=8)
    ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=16, weight="bold"), anchor="w").grid(
        row=0, column=0, columnspan=2, padx=8, pady=(8, 2), sticky="ew"
    )
    return frame


def _entry_with_details(
    parent: ctk.CTkFrame, label: str, default: str, details: str, row: int, col: int
) -> ctk.CTkEntry:
    ctk.CTkLabel(parent, text=label, anchor="w").grid(row=row, column=col, padx=8, pady=(8, 0), sticky="ew")
    ctk.CTkLabel(parent, text=details, anchor="w", text_color="gray70", justify="left", wraplength=760).grid(
        row=row + 1, column=col, padx=8, pady=(0, 0), sticky="ew"
    )
    entry = ctk.CTkEntry(parent)
    entry.grid(row=row + 2, column=col, padx=8, pady=(2, 8), sticky="ew")
    entry.insert(0, default)
    return entry


def _switch_with_details(
    parent: ctk.CTkFrame, label: str, details: str, row: int, command: object | None = None
) -> ctk.CTkSwitch:
    switch = ctk.CTkSwitch(parent, text=label, command=command)
    switch.grid(row=row, column=0, columnspan=2, padx=8, pady=(8, 2), sticky="w")
    ctk.CTkLabel(parent, text=details, anchor="w", text_color="gray70", justify="left", wraplength=760).grid(
        row=row + 1, column=0, columnspan=2, padx=8, pady=(0, 6), sticky="ew"
    )
    return switch


def _set_entry(entry: ctk.CTkEntry, value: str) -> None:
    entry.delete(0, "end")
    entry.insert(0, value)


def _set_switch(switch: ctk.CTkSwitch, enabled: bool) -> None:
    if enabled:
        switch.select()
    else:
        switch.deselect()


def _set_entry_state(entry: ctk.CTkEntry, enabled: bool) -> None:
    if enabled:
        entry.configure(state="normal")
    else:
        entry.configure(state="disabled")


def run_gui() -> int:
    app = AutoClickerApp()
    app.mainloop()
    return 0
