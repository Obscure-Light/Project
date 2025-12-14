# Risolutore IP-Hostname

Questo progetto fornisce una semplice interfaccia grafica per risolvere indirizzi IP o nomi di dominio:
- Se la riga di input è un **hostname** (es. `example.com`), il programma ne risolve l'IP.
- Se la riga è già un **indirizzo IP** (es. `8.8.8.8`), il programma prova a trovare il relativo hostname.

I risultati vengono salvati in un file **Excel** con tre colonne:
1. **Input** originale (hostname o IP)  
2. **IP** risolto  
3. **Hostname** trovato  

Se la risoluzione non è possibile, nella colonna "Hostname" apparirà la scritta "Campo non trovato".

## Struttura del progetto
- **main.py**: Punto di ingresso; avvia l'applicazione chiamando `start_app()`.
- **gui.py**: Gestisce l'interfaccia grafica (Tkinter), la selezione dei file input e output, e utilizza le funzioni di risoluzione.
- **resolver.py**: Include la logica per la risoluzione IP/hostname (`resolve_addresses`) e la creazione del file Excel (`save_to_excel`).
- **requirements.txt** (opzionale): Elenca eventuali dipendenze specifiche. Qui è probabile che tu debba includere `openpyxl`.

## Requisiti
- **Python 3.x**
- **Tkinter** (di solito incluso in molte installazioni Python, ma potrebbe dover essere installato separatamente su alcune piattaforme).
- **openpyxl** (per creare file Excel).

Per installare `openpyxl`, se non presente:
```bash
pip install openpyxl
```

