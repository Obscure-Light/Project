# Autoclicker

Tool di automazione tastiera in Python con doppia interfaccia:
- GUI in italiano (`customtkinter`)
- CLI completa (`argparse`)

Il progetto usa un motore unico condiviso (`autoclicker/core/engine.py`) per garantire coerenza tra UI e CLI.

## Funzionalita principali

- Tasto singolo o combinazione (`numlock`, `ctrl+shift+x`, ...)
- Click mouse singolo/doppio (`mouse_left`, `mouse_left_double`, ...)
- Scroll mouse (`mouse_scroll_up`, `mouse_scroll_down`) con step configurabile
- Intervallo base configurabile (default `300` secondi)
- Randomizzazione "umana" gaussiana attivabile/disattivabile
- Finestra oraria attivabile/disattivabile (supporta anche intervalli oltre mezzanotte)
- Limite numero pressioni attivabile/disattivabile
- Delay iniziale attivabile/disattivabile
- Delay tra tasti per combinazioni
- Modalita `dry-run` (simulazione senza invio tasti)
- Salvataggio/caricamento profilo JSON
- Log eventi e stato runtime

## Struttura progetto

```text
Autoclicker/
  autoclicker/
    core/
      config.py
      engine.py
      keyboard_sender.py
      randomizer.py
    interfaces/
      cli.py
      gui.py
  main.py
  requirements.txt
  README.md
```

## Requisiti

- Python 3.10+
- Windows (testato per uso desktop)

Installazione dipendenze:

```bash
pip install -r requirements.txt
```

## Avvio

GUI:

```bash
python main.py
```

CLI:

```bash
python main.py --key numlock --interval 300
```

## Esempi CLI

Randomizzazione umana ON:

```bash
python main.py --key numlock --interval 300 --randomization on --random-stddev 5 --random-min -10 --random-max 10
```

Combinazione tasti e finestra oraria:

```bash
python main.py --key ctrl+shift+x --interval 120 --time-window on --start-time 09:00 --end-time 18:00
```

Click mouse:

```bash
python main.py --key mouse_left --interval 10
```

Doppio click mouse:

```bash
python main.py --key mouse_left_double --interval 10
```

Scroll mouse:

```bash
python main.py --key mouse_scroll_down --mouse-scroll-steps 3 --interval 5
```

Nota: le azioni mouse sono singole (`mouse_left`, `mouse_left_double`, `mouse_scroll_up`), non in combinazione con tasti.

Limite ripetizioni e delay iniziale:

```bash
python main.py --key numlock --interval 300 --repeat on --repeat-count 20 --initial-delay on --initial-delay-seconds 5
```

Simulazione senza invio tasti:

```bash
python main.py --key numlock --interval 30 --dry-run
```

Salva/carica profilo:

```bash
python main.py --save-config profile.json --key numlock --interval 300
python main.py --config profile.json
```

Nota: quando usi `--config`, i parametri passati esplicitamente via CLI hanno priorita sul file.

## Build EXE (opzionale)

Installazione `pyinstaller`:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed --name Autoclicker main.py
```

Output in `dist/Autoclicker.exe`.

## Test

Esegui i test automatici:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Note d'uso

- Usa il tool solo per automazioni consentite nel tuo contesto.
- Verifica sempre la configurazione con `--dry-run` prima dell'uso reale.
