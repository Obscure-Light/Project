# YouTube Playlist Downloader

Questo progetto consente di scaricare l'intera playlist di YouTube presente in uno o più URL, grazie alla libreria `pytube`.

## Requisiti

- **Python** 3.7 o successivo  
- **pip** per installare le dipendenze  

## Installazione

1. Clona questo repository o scarica lo ZIP

2. Installa le dipendenze con:  
   pip install -r requirements.txt

---

## Utilizzo

1. Crea un file di testo con uno o più URL di playlist di YouTube, ognuno su una riga. Ad esempio:  
   https://www.youtube.com/playlist?list=PLxxxxxx
   https://www.youtube.com/playlist?list=PLyyyyyy

2. Aggiorna `main.py`: imposta la variabile `urls_file_path` con il percorso del tuo file di testo, ad esempio:  
   urls_file_path = "percorsi_playlist.txt"

3. Esegui il programma con:  
   python main.py

4. Controlla i risultati:  
   - I video verranno scaricati in una cartella con il nome della playlist.  
   - Oppure, se hai specificato una cartella personalizzata, i file verranno salvati lì.

---

## Utilizzo avanzato

### Destinazione personalizzata  
Se vuoi salvare tutti i video di una playlist in una cartella specifica, puoi passare un secondo parametro a `download_youtube_playlist(url)`.  

Esempio:  
   download_youtube_playlist(url, output_folder="CartellaPersonalizzata")

Se non imposti `output_folder`, verrà usato il titolo della playlist come nome della cartella.

---

### Supporto per più file di testo  
Se hai più file di testo con diverse liste di URL, puoi gestirli uno dopo l'altro semplicemente richiamando:  
   read_urls_from_file("file1.txt")
   download_youtube_playlist(url_list)
   read_urls_from_file("file2.txt")
   download_youtube_playlist(url_list)

---

### Argomenti da riga di comando  
Per maggiore flessibilità, puoi usare `argparse` in `main.py` per leggere i percorsi di input e la cartella di destinazione come parametri.

Esempio di esecuzione con argomenti:  
   python main.py --input percorsi_playlist.txt --output "Download/Playlist"

Nota: Se vuoi questa funzionalità, assicurati che `argparse` sia implementato nel codice.

---

## Contributi e miglioramenti  
Ogni suggerimento è ben accetto! Se vuoi contribuire, apri una **issue** o una **pull request**. 🚀
