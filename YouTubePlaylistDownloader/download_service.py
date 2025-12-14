# download_service.py

from pytube import Playlist


def download_youtube_playlist(url: str, output_folder: str = "") -> None:
    """
    Scarica tutti i video da una playlist di YouTube.

    :param url: L'URL della playlist di YouTube
    :param output_folder: Cartella di destinazione per i video scaricati
    :return: None
    """
    try:
        playlist = Playlist(url)
    except Exception as exc:
        print(f"Errore durante l'inizializzazione della playlist: {exc}")
        return

    # Se non viene fornita una cartella di output, usiamo come default il titolo della playlist.
    if not output_folder:
        output_folder = playlist.title

    # Iteriamo su tutti i video nella playlist e li scarichiamo.
    for video in playlist.videos:
        try:
            print(f"Downloading: {video.title}")
            stream = video.streams.get_highest_resolution()
            stream.download(output_path=output_folder)
            print(f"{video.title} downloaded successfully!")
        except Exception as e:
            print(f"Errore durante il download di {video.title}: {str(e)}")


def read_urls_from_file(file_path: str) -> list[str]:
    """
    Legge un file di testo contenente URL (uno per riga) e li restituisce come lista.

    :param file_path: Percorso del file di testo con gli URL.
    :return: Lista di URL estratti dal file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"Il file non esiste: {file_path}")
        return []
    except Exception as exc:
        print(f"Errore durante la lettura del file: {exc}")
        return []