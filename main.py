import argparse
import sys
from pathlib import Path

from photo_organizer.directory_scanner import DirectoryScanner


def existing_dir(path_str):
    """
    Validate and convert a path string to a resolved Path object.

    Args:
        path_str (str): The path string to validate

    Returns:
        Path: A resolved Path object pointing to an existing directory

    Raises:
        argparse.ArgumentTypeError: If the path doesn't exist or isn't a directory
    """
    path = Path(path_str).expanduser().resolve()

    if not path.exists():
        raise argparse.ArgumentTypeError(f"Directory does not exist: {path}")

    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"Path is not a directory: {path}")

    return path


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
        type=existing_dir,
        help="A pasta de origem a ser analisada.",
    )
    args = parser.parse_args()

    source_path = args.source_folder

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
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
