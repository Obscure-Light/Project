"""
Modulo calculator
-----------------
Contiene le funzioni che eseguono i vari calcoli:
- scorporo_iva
- calcola_preventivi
- calcola_vendita_componenti
- sconto_dal_prezzo_netto
- calcola_lordo
- sconto_dal_prezzo_lordo
- calcola_budget_giornaliero

Ogni funzione riceve in input i valori necessari e restituisce i risultati
da stampare o utilizzare in altre parti del programma.
"""

def scorporo_iva(importo: float, aliquota: float = 22.0) -> tuple[float, float]:
    """
    Calcola l'importo senza IVA e l'IVA scorporata da un importo lordo.
    
    :param importo: L'importo lordo, comprensivo di IVA.
    :param aliquota: Percentuale IVA, di default 22%.
    :return: (importo_scorporato, iva).
    """
    # Ad esempio, se aliquota = 22, e importo è 122, l'importo senza IVA è 100
    # e l'IVA è 22.
    importo_scorporato = round(importo * 100 / (100 + aliquota))
    iva = importo - importo_scorporato
    return importo_scorporato, iva

def calcola_preventivi(importo_netto: float, aliquota: float = 22.0) -> dict:
    """
    Calcola diversi possibili preventivi aggiungendo un valore fisso all'importo netto
    e poi calcolando l'importo lordo (con IVA).
    
    :param importo_netto: Importo netto iniziale.
    :param aliquota: Percentuale IVA (default 22%).
    :return: Dizionario con i valori di importo lordo, IVA e 4 proposte di preventivo.
    """
    coeff_iva = 1 + aliquota/100
    importo_lordo = round(importo_netto * coeff_iva, 2)
    iva = round(importo_lordo - importo_netto, 2)
    
    preventivi = {}
    # Puoi personalizzare gli incrementi (30, 35, 40, 50) come preferisci
    for i, incremento in enumerate([30, 35, 40, 50], start=1):
        preventivi[f"preventivo_{i}"] = round((importo_netto + incremento) * coeff_iva, 2)

    return {
        "importo_lordo": importo_lordo,
        "iva": iva,
        **preventivi
    }

def calcola_vendita_componenti(importo_netto: float, ricarico: float = 15.0, aliquota: float = 22.0) -> tuple[float, float]:
    """
    Calcola l'importo lordo e il prezzo di vendita (aggiungendo un ricarico fisso prima dell'IVA).
    
    :param importo_netto: Importo netto iniziale.
    :param ricarico: Ricarico fisso da aggiungere all'importo netto.
    :param aliquota: Percentuale IVA (default 22%).
    :return: (prezzo_lordo, prezzo_vendita).
    """
    coeff_iva = 1 + aliquota / 100
    prezzo_lordo = importo_netto * coeff_iva
    prezzo_vendita = (importo_netto + ricarico) * coeff_iva
    return prezzo_lordo, prezzo_vendita

def sconto_dal_prezzo_netto(importo_netto: float, sconto_perc: float, aliquota: float = 22.0) -> dict:
    """
    Applica uno sconto percentuale a partire da un importo netto:
    1. Calcola l'importo ivato
    2. Calcola la riduzione in valore assoluto
    3. Restituisce l'importo scontato
    
    :param importo_netto: Importo netto iniziale.
    :param sconto_perc: Percentuale di sconto da applicare.
    :param aliquota: Percentuale IVA (default 22%).
    :return: Dizionario con importo ivato, valore dello sconto, importo scontato.
    """
    coeff_iva = 1 + aliquota / 100
    importo_ivato = importo_netto * coeff_iva
    sconto_valore = importo_ivato * sconto_perc / 100
    importo_scontato = importo_ivato - sconto_valore
    
    return {
        "importo_ivato": importo_ivato,
        "sconto_valore": sconto_valore,
        "importo_scontato": importo_scontato
    }

def calcola_lordo(importo_netto: float, aliquota: float = 22.0) -> float:
    """
    Calcola l'importo lordo partendo da un importo netto.
    
    :param importo_netto: Importo netto iniziale.
    :param aliquota: Percentuale IVA (default 22%).
    :return: L'importo lordo (netto + IVA).
    """
    coeff_iva = 1 + aliquota / 100
    return importo_netto * coeff_iva

def sconto_dal_prezzo_lordo(importo_lordo: float, sconto_perc: float) -> dict:
    """
    Applica uno sconto percentuale a partire da un importo lordo.
    
    :param importo_lordo: Importo lordo di partenza.
    :param sconto_perc: Percentuale di sconto da applicare.
    :return: Dizionario con valore dello sconto e importo scontato.
    """
    sconto_valore = importo_lordo * sconto_perc / 100
    importo_scontato = importo_lordo - sconto_valore
    return {
        "sconto_valore": sconto_valore,
        "importo_scontato": importo_scontato
    }

def calcola_budget_giornaliero(fatturato_precedente: float, numero_dipendenti: int, ore_lavoro: float) -> dict:
    """
    Calcola il budget giornaliero sulla base del fatturato di un giorno analogo (es. stessa giornata della settimana precedente).
    
    :param fatturato_precedente: Fatturato registrato in una giornata di riferimento.
    :param numero_dipendenti: Numero di dipendenti in attività.
    :param ore_lavoro: Ore di lavoro previste.
    :return: Dizionario con la media oraria e il budget target da superare.
    """
    # Divisione per 12 come nel calcolo originale (ad esempio 12 ore di apertura standard)
    media_vendite = fatturato_precedente / 12 / numero_dipendenti
    budget_da_superare = media_vendite * ore_lavoro

    return {
        "media_oraria": media_vendite,
        "budget_da_superare": budget_da_superare
    }
