"""
File principale (main.py)
-------------------------
Punto di ingresso dell'applicazione. Gestisce l'interfaccia testuale,
le scelte dell'utente e richiama le funzioni di calcolo dal modulo 'calculator'.
"""

import sys
import calculator

def main():
    while True:
        print("""
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    Programma di calcolo costi, preventivi, scorporo IVA, sconti e budget.
    ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    Scegli una delle seguenti funzioni:
    [1] Scorporo IVA
    [2] Calcolo di un preventivo
    [3] Calcolo di vendita componenti
    [4] Sconto sul prezzo netto
    [5] Calcolo dell'importo lordo
    [6] Sconto sul prezzo lordo
    [7] Calcolo del budget giornaliero
    [esc] Esci dal programma
        """)

        scelta = input("Inserisci il numero corrispondente ---> ").strip().lower()

        if scelta == "1":
            print("\nHai scelto: Scorporo IVA")
            try:
                importo = float(input("Scrivi l'importo lordo da scorporare --->  "))
            except ValueError:
                print("Valore non valido. Riprova.")
                continue
            
            importo_scorporato, iva = calculator.scorporo_iva(importo)
            print(f"L'importo scorporato è di euro {importo_scorporato}")
            print(f"L'IVA è di euro {iva}")

        elif scelta == "2":
            print("\nHai scelto: Calcolo di un preventivo")
            try:
                importo_netto = float(input("Scrivi l'importo netto del pezzo --->  "))
            except ValueError:
                print("Valore non valido. Riprova.")
                continue
            
            risultati = calculator.calcola_preventivi(importo_netto)
            print(f"L'importo lordo è di euro {risultati['importo_lordo']}")
            print(f"L'IVA è di euro {risultati['iva']}")
            
            # Stampa delle proposte
            for i in range(1, 5):
                key = f"preventivo_{i}"
                print(f"Proposta preventivo N° {i}: {risultati[key]}")

        elif scelta == "3":
            print("\nHai scelto: Vendita componenti")
            try:
                importo_netto = float(input("Scrivi l'importo netto del pezzo ---> "))
            except ValueError:
                print("Valore non valido. Riprova.")
                continue
            
            prezzo_lordo, prezzo_vendita = calculator.calcola_vendita_componenti(importo_netto)
            print(f"Il prezzo lordo è di euro {prezzo_lordo:.2f}")
            print(f"Il prezzo di vendita è di euro {prezzo_vendita:.2f}")

        elif scelta == "4":
            print("\nHai scelto: Sconto sul prezzo netto")
            try:
                importo_netto = float(input("Inserisci l'importo netto da scontare ---> "))
                sconto_perc = float(input("Inserisci lo sconto in percentuale da effettuare ---> "))
            except ValueError:
                print("Valore non valido. Riprova.")
                continue
            
            risultati = calculator.sconto_dal_prezzo_netto(importo_netto, sconto_perc)
            print(f"L'importo ivato è di euro {risultati['importo_ivato']:.2f}")
            print(f"Lo sconto è di euro {risultati['sconto_valore']:.2f}")
            print(f"L'importo scontato è di euro {risultati['importo_scontato']:.2f}")

        elif scelta == "5":
            print("\nHai scelto: Calcolo dell'importo lordo")
            try:
                importo_netto = float(input("Inserisci l'importo netto ---> "))
            except ValueError:
                print("Valore non valido. Riprova.")
                continue
            
            importo_lordo = calculator.calcola_lordo(importo_netto)
            print(f"L'importo lordo è di euro {importo_lordo:.2f}")

        elif scelta == "6":
            print("\nHai scelto: Sconto sul prezzo lordo")
            try:
                importo_lordo = float(input("Inserisci l'importo lordo da scontare ---> "))
                sconto_perc = float(input("Inserisci lo sconto in percentuale da effettuare --->  "))
            except ValueError:
                print("Valore non valido. Riprova.")
                continue

            risultati = calculator.sconto_dal_prezzo_lordo(importo_lordo, sconto_perc)
            print(f"Lo sconto è di euro {risultati['sconto_valore']:.2f}")
            print(f"L'importo scontato è di euro {risultati['importo_scontato']:.2f}")

        elif scelta == "7":
            print("\nHai scelto: Calcolo del budget giornaliero")
            try:
                fatturato_precedente = float(input("Inserisci il fatturato della giornata di riferimento --->  "))
                numero_dipendenti = int(input("Inserisci il numero dei dipendenti --->  "))
                ore_lavoro = float(input("Inserisci le ore di lavoro previste --->  "))
            except ValueError:
                print("Valore non valido. Riprova.")
                continue

            risultati = calculator.calcola_budget_giornaliero(fatturato_precedente, numero_dipendenti, ore_lavoro)
            print(f"Media di vendite per ogni ora: {risultati['media_oraria']:.2f}")
            print(f"Il tuo budget da superare è di euro {risultati['budget_da_superare']:.2f}")

        elif scelta == "esc":
            print("Uscita dal programma.")
            sys.exit(0)

        else:
            print("Scelta non valida. Riprova.")
            continue

        # Chiedi all'utente se continuare
        loop = input("\nSe vuoi continuare ad usare l'applicazione digita 'si', altrimenti premi Invio per uscire. ")
        if loop.lower() != "si":
            print("Grazie per aver utilizzato il programma. Alla prossima!")
            break

if __name__ == "__main__":
    main()
