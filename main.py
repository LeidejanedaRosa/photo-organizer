import argparse
import sys
from pathlib import Path

from photo_organizer.directory_scanner import DirectoryScanner


def main():
    """
    Ponto de entrada principal da aplicação.

    Coordena a análise do diretório e a exibição dos arquivos encontrados.
    """
    parser = argparse.ArgumentParser(
        description="Organiza fotos e outros arquivos em uma pasta."
    )
    parser.add_argument(
        "source_folder",
        type=str,
        help="A pasta de origem a ser analisada.",
    )
    args = parser.parse_args()

    source_path = Path(args.source_folder)

    try:
        scanner = DirectoryScanner(source_path)
        files = scanner.scan_files()

        print(f"Analisando a pasta: {source_path}")
        if not files:
            print("Nenhum arquivo encontrado.")
        else:
            for file in files:
                print(file)

    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
