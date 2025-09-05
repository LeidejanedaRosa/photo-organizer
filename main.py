import argparse
import sys
from pathlib import Path


def existing_dir(path_str):

    path = Path(path_str).expanduser().resolve()

    if not path.exists():
        raise argparse.ArgumentTypeError(f"Directory does not exist: {path}")

    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"Path is not a directory: {path}")

    return path


def main():

    parser = argparse.ArgumentParser(
        description="Organiza fotos e outros arquivos em uma pasta."
    )
    parser.add_argument(
        "source_folder",
        type=existing_dir,
        help="A pasta de origem a ser analisada.",
    )
    parser.add_argument(
        "--organize",
        action="store_true",
        help="Organiza os arquivos em pastas por tipo (Videos, Textos, Outros). Imagens permanecem na pasta atual.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Retorna o resultado em formato JSON (útil para integração com frontend).",
    )
    args = parser.parse_args()

    try:
        from photo_organizer.controller import PhotoOrganizerController

        controller = PhotoOrganizerController()

        if args.organize:
            result = controller.organize_files_endpoint(
                folder_path=str(args.source_folder), organize=True
            )
        else:
            result = controller.analyze_folder_endpoint(str(args.source_folder))

        if args.json:
            import json

            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            _print_cli_output(result, args.organize, str(args.source_folder))

    except Exception as e:
        if hasattr(args, "json") and args.json:
            import json

            error_result = {
                "success": False,
                "message": f"Erro inesperado: {str(e)}",
                "data": {},
                "errors": [str(e)],
            }
            print(json.dumps(error_result, indent=2, ensure_ascii=False))
        else:
            print(f"Erro inesperado: {e}", file=sys.stderr)
        sys.exit(1)


def _print_cli_output(result: dict, organize_mode: bool, source_folder: str):
    """Formata a saída para linha de comando."""
    if not result["success"]:
        print(f"Erro: {result['message']}", file=sys.stderr)
        return

    data = result["data"]
    print(f"Analisando a pasta: {source_folder}")

    if data["total_files"] == 0:
        print("Nenhum arquivo encontrado.")
        return

    print(f"\nArquivos encontrados ({data['total_files']}):")
    for file_info in data["files"]:
        print(f"  • Arquivo: {file_info['name']} - Tipo: {file_info['type']}")

    if organize_mode and "organization_summary" in data:
        print("\n" + "=" * 50)
        print("INICIANDO ORGANIZAÇÃO DOS ARQUIVOS...")
        print("=" * 50)

        # Simula o feedback de movimento (já foi feito pelo service)
        summary = data["organization_summary"]

        print("\n=== RESUMO DA ORGANIZAÇÃO ===")
        if data.get("folders_created"):
            print(f"Pastas criadas: {', '.join(data['folders_created'])}")
        else:
            print("Nenhuma pasta nova foi criada.")

        print(f"Total de arquivos analisados: {summary['total_analyzed']}")

        if summary["moved_by_type"]:
            print("Arquivos movidos:")
            for file_type, count in summary["moved_by_type"].items():
                folder_name = _get_folder_name(file_type)
                print(f"  • {count} arquivo(s) de {file_type} -> {folder_name}/")
        else:
            print("Nenhum arquivo foi movido.")

        if summary["images_remaining"] > 0:
            print(
                f"  • {summary['images_remaining']} imagem(ns) permaneceu(ram) na pasta atual"
            )
    elif not organize_mode:
        print("\nPara organizar os arquivos em pastas, execute:")
        print(f'python main.py "{source_folder}" --organize')


def _get_folder_name(file_type: str) -> str:
    """Retorna o nome da pasta para um tipo de arquivo."""
    mapping = {"Vídeo": "Videos", "Texto": "Textos", "Outro": "Outros"}
    return mapping.get(file_type, "Outros")


if __name__ == "__main__":
    main()
