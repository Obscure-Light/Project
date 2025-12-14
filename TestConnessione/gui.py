import tkinter as tk
from tkinter import messagebox

from connection_tester import test_tcp_connection, test_udp_connection

def test_connection(entry_ip: tk.Entry, entry_port: tk.Entry, protocol_var: tk.IntVar) -> None:
    """
    Funzione che, in base al protocollo scelto (TCP o UDP), richiama le rispettive funzioni di test.

    :param entry_ip: Campo di testo per l’IP
    :param entry_port: Campo di testo per la porta
    :param protocol_var: Variabile che indica il protocollo selezionato (1 per TCP, 2 per UDP)
    """
    ip = entry_ip.get().strip()
    port_str = entry_port.get().strip()

    if not ip or not port_str.isdigit():
        messagebox.showerror("Errore", "Inserisci un IP e una porta validi.")
        return

    port = int(port_str)
    if port <= 0:
        messagebox.showerror("Errore", "La porta deve essere un numero positivo.")
        return

    if protocol_var.get() == 1:  # TCP
        test_tcp_connection(ip, port)
    elif protocol_var.get() == 2:  # UDP
        test_udp_connection(ip, port)
    else:
        messagebox.showwarning("Protocollo non selezionato", "Seleziona TCP o UDP.")

def create_gui() -> None:
    """
    Crea la finestra principale dell’applicazione e ne gestisce l’interfaccia grafica.
    """
    root = tk.Tk()
    root.title("Test di Connessione")
    root.geometry("300x250")

    protocol_var = tk.IntVar()

    label_protocol = tk.Label(root, text="Seleziona il protocollo:")
    label_protocol.pack(pady=5)

    radio_tcp = tk.Radiobutton(
        root,
        text="TCP",
        variable=protocol_var,
        value=1
    )
    radio_tcp.pack()

    radio_udp = tk.Radiobutton(
        root,
        text="UDP",
        variable=protocol_var,
        value=2
    )
    radio_udp.pack()

    label_ip = tk.Label(root, text="Inserisci l'IP:")
    label_ip.pack(pady=5)

    entry_ip = tk.Entry(root)
    entry_ip.pack()

    label_port = tk.Label(root, text="Inserisci la porta:")
    label_port.pack(pady=5)

    entry_port = tk.Entry(root)
    entry_port.pack()

    button_test = tk.Button(
        root,
        text="Test Connessione",
        command=lambda: test_connection(entry_ip, entry_port, protocol_var)
    )
    button_test.pack(pady=10)

    root.mainloop()
