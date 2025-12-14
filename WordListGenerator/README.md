# Password Combination Generator

Un semplice generatore di combinazioni di password basato su lunghezza minima e massima e su un set di caratteri selezionabili dall'utente.

## Caratteristiche

- Possibilità di generare combinazioni con diverse lunghezze (minima e massima).
- Supporto a vari set di caratteri: lettere maiuscole, minuscole, numeri, caratteri speciali e combinazioni di questi.
- Salvataggio dei risultati in un file di testo (`passlist.txt`).

## Struttura del progetto


- **combo_generator.py**: Contiene la funzione `generate_combinations` che crea tutte le possibili combinazioni di caratteri.
- **main.py**: Script principale che gestisce l'interazione con l'utente e chiama la funzione di generazione combinazioni.
- **requirements.txt**: Elenco delle eventuali dipendenze (se presenti).
- **README.md**: Questo file, contenente la documentazione e le istruzioni d'uso.

## Requisiti

- Python 3.7 o superiore.
- Nessuna libreria esterna necessaria (usa solo librerie standard: `itertools`, `string`).

## Installazione

1. **Clona il repository** o scarica lo zip.
2. **(Facoltativo)** Crea e attiva un ambiente virtuale:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate         # Windows



Utilizzo
Dal terminale, posizionati nella cartella del progetto:
cd WordListGenerator

Esegui lo script principale:
python main.py

Segui le istruzioni fornite a schermo:
Inserisci la lunghezza minima e massima.
Seleziona il tipo di set di caratteri da utilizzare.
Attendi la generazione delle combinazioni. Al termine, verrà creato un file passlist.txt nella stessa cartella, contenente tutte le possibili combinazioni.

Esempio di Esecuzione

Password Combination Generator
-----------------------------
Inserisci la lunghezza minima delle password: 1
Inserisci la lunghezza massima delle password: 2

Seleziona il tipo di caratteri da usare:
1. Lettere maiuscole
2. Lettere minuscole
3. Lettere maiuscole e minuscole
4. Numeri e lettere (maiuscole e minuscole)
5. Solo numeri
6. Caratteri speciali e lettere (maiuscole e minuscole)
7. Tutti i caratteri (lettere, numeri, caratteri speciali)
Inserisci il numero corrispondente alla tua scelta: 4

Combinazioni generate e salvate in: passlist.txt