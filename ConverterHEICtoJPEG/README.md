"""
# HEIC to JPEG Converter

Questo progetto permette di convertire facilmente immagini in formato HEIC in formato JPEG, sfruttando le librerie **pyheif** e **Pillow**.

## Requisiti
- Python 3.x
- pyheif
- Pillow
- (facoltativo) argparse se non già presente nella distribuzione di Python.

## Installazione
1. Clonare il repository GitHub o scaricare i file di questo progetto.
2. Installare le dipendenze:
   ```
   pip install -r requirements.txt
   ```

## Utilizzo
### Da riga di comando
Eseguire lo script **main.py** specificando i parametri:
```bash
python main.py --input "percorso/del/file.heic" --output "percorso/del/file_output.jpg"
```
- `--input` (richiesto): il percorso del file HEIC di input.
- `--output` (opzionale): il percorso e nome desiderati per il file JPEG risultante. Predefinito: `output_image.jpg`.

### Come modulo Python
In uno script Python:
```python
from converter import convert_heic_to_jpeg

convert_heic_to_jpeg("percorso/del/file.heic", "percorso/del/file_output.jpg")
```

## Struttura del progetto
- **converter.py**: Modulo con la funzione che si occupa della conversione.
- **main.py**: Script principale che gestisce la riga di comando e invoca la funzione.
- **requirements.txt**: Elenco delle librerie necessarie.
- **README.md**: Documentazione del progetto.

## Licenza
Questo progetto è fornito sotto licenza MIT. Consulta il file LICENSE per maggiori dettagli.
"""