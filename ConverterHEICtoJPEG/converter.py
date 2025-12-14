"""
Modulo di conversione delle immagini HEIC in JPEG.

Contiene la funzione "convert_heic_to_jpeg" che si occupa della lettura del
file HEIC e della conversione in un'immagine JPEG, tramite la libreria Pillow (PIL) e pyheif.

Esempio d'uso:
    from converter import convert_heic_to_jpeg
    convert_heic_to_jpeg("percorso/del/file.heic", "percorso/del/file_output.jpg")
"""

import pyheif
from PIL import Image


def convert_heic_to_jpeg(input_path: str, output_path: str) -> None:
    """
    Converte un'immagine HEIC in formato JPEG.

    :param input_path: Percorso del file .heic di input.
    :param output_path: Percorso del file di output .jpg.
    :return: None.
    """
    # Legge il file HEIC utilizzando pyheif
    heif_file = pyheif.read(input_path)

    # Crea un oggetto immagine PIL a partire dai dati HEIC
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

    # Salva l'immagine come JPEG con qualità 100
    image.save(output_path, format="JPEG", quality=100)