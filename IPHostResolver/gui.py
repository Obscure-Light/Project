import tkinter as tk
from tkinter import filedialog, messagebox

from resolver import resolve_addresses, save_to_excel

def select_files_and_resolve():
    """
    Apre finestre di dialogo per la selezione del file di input (testo)
    e del file di output (Excel), poi richiama le funzioni per risolvere
    gli IP/hostname e salvare i risultati.
    """
    input_file = filedialog.askopenfilename(
        title="Seleziona il file di input",
        filetypes=(("File di testo", "*.txt"), ("Tutti i file", "*.*"))
    )

    if not input_file:
        return

    output_file = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=(("File Excel", "*.xlsx"), ("Tutti i file", "*.*")),
        title="Salva come"
    )

    if not output_file:
        return

    try:
        # Lettura degli indirizzi o host dal file di input
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Risoluzione
        results = resolve_addresses(lines)

        # Salvataggio su Excel
        save_to_excel(results, output_file)

        messagebox.showinfo(
            "Completato",
            "Risoluzione completata. File salvato con successo!"
        )

    except Exception as e:
        messagebox.showerror(
            "Errore",
            f"Si è verificato un errore durante la risoluzione:\n{e}"
        )

def create_gui():
    """
    Crea la finestra principale dell'applicazione, con un pulsante
    per avviare il processo di risoluzione.
    """
    root = tk.Tk()
    root.title("Risoluzione IP e Hostname")
    root.geometry("300x100")

    button = tk.Button(
        root,
        text="Seleziona file",
        command=select_files_and_resolve
    )
    button.pack(pady=20)

    root.mainloop()
