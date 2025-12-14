import socket
from tkinter import messagebox

def test_tcp_connection(ip_address: str, port: int) -> None:
    """
    Tenta di connettersi via TCP al server specificato.

    :param ip_address: Indirizzo IP del server
    :param port: Porta del server
    :return: Nessun valore di ritorno, genera un messaggio all’utente tramite tkinter
    """
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_socket.connect((ip_address, port))
        messagebox.showinfo(
            "Connessione TCP",
            f"Connessione TCP riuscita a {ip_address}:{port}"
        )
    except socket.error as error:
        messagebox.showerror(
            "Errore TCP",
            f"Connessione TCP fallita: {error}"
        )
    finally:
        tcp_socket.close()

def test_udp_connection(ip_address: str, port: int) -> None:
    """
    Invia un semplice messaggio (Test) via UDP all’IP e porta specificati.

    :param ip_address: Indirizzo IP del server
    :param port: Porta del server
    :return: Nessun valore di ritorno, genera un messaggio all’utente tramite tkinter
    """
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Invia un messaggio di test
        udp_socket.sendto(b"Test", (ip_address, port))
        messagebox.showinfo(
            "Connessione UDP",
            f"Test UDP inviato a {ip_address}:{port}"
        )
    except socket.error as error:
        messagebox.showerror(
            "Errore UDP",
            f"Invio UDP fallito: {error}"
        )
    finally:
        udp_socket.close()
