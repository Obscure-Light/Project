# main.py

from download_service import download_youtube_playlist, read_urls_from_file


def main():
    """
    Punto di ingresso dell'applicazione.
    """
    # Percorso del file di testo contenente gli URL delle playlist.
    # (Modifica qui con il percorso corretto del tuo file, ad esempio 'percorsi_playlist.txt')
    urls_file_path = "percorsi_playlist.txt"

    # Leggiamo la lista di URL dal file
    playlist_urls = read_urls_from_file(urls_file_path)

    # Per ogni URL, effettuiamo il download della playlist
    for url in playlist_urls:
        if url:  # Assicurarsi che la stringa non sia vuota
            download_youtube_playlist(url)


if __name__ == "__main__":
    main()