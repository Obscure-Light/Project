"""
Script principale per la conversione di un file HEIC in JPEG.
Si appoggia al modulo "converter.py" per la logica di conversione.

Esempio di utilizzo:
    python main.py --input "percorso/del/file.heic" --output "percorso/del/file_output.jpg"

"""

import argparse
from converter import convert_heic_to_jpeg


def main() -> None:
    # Definisci i parametri da riga di comando
    parser = argparse.ArgumentParser(
        description="Script per convertire immagini HEIC in JPEG"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Percorso del file HEIC di input"
    )
    parser.add_argument(
        "--output",
        default="output_image.jpg",
        help="Percorso del file JPG di output (predefinito: output_image.jpg)"
    )

    args = parser.parse_args()

    # Esegue la conversione utilizzando la funzione del modulo converter
    convert_heic_to_jpeg(args.input, args.output)

    print(f"Conversione completata! File salvato in: {args.output}")


if __name__ == "__main__":
    main()