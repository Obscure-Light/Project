# Programma di Calcolo e Preventivi

Questo progetto è un’applicazione da riga di comando (CLI) che permette di eseguire vari calcoli commerciali, fra cui:

- **Scorporo IVA**  
- **Calcolo di preventivi** (con varie proposte)  
- **Calcolo di prezzi di vendita componenti** (aggiungendo un ricarico fisso)  
- **Applicazione di sconti** (su importo netto o lordo)  
- **Calcolo di budget giornaliero** (in base al fatturato storico)

---

## Struttura del progetto

- **`calculator.py`**  
  Contiene tutte le funzioni di calcolo. Ogni funzione riceve parametri in ingresso (ad es. `importo_netto`, `sconto_perc`, ecc.) e restituisce i risultati dei calcoli.

- **`main.py`**  
  File principale che si occupa di:
  1. Mostrare il menu di scelta delle operazioni.  
  2. Richiedere gli input all’utente.  
  3. Invocare le funzioni appropriate all’interno di `calculator.py`.  
  4. Visualizzare i risultati.

- **`README.md`**  
  Il file che stai leggendo, contenente la documentazione e una guida rapida all’uso del programma.

---

## Installazione e Requisiti

1. **Clona** la repository o scarica i file in una cartella sul tuo computer.
2. Assicurati di avere installato **Python 3.7+** (in versioni precedenti potrebbe comunque funzionare, ma si consiglia una versione recente).
3. Non sono richieste librerie aggiuntive oltre a quelle standard di Python.

---

## Come Eseguire il Programma

1. Apri un terminale (o prompt dei comandi).
2. Posizionati nella cartella in cui hai salvato i file (`main.py`, `calculator.py`, ecc.).
3. Lancia il comando:

   ```bash
   python main.py
