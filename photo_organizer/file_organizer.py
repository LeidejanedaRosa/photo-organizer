import shutil
from pathlib import Path
from typing import Dict, List

from .file_handler import FileHandler


class FileOrganizer:

    def __init__(self, base_directory: Path):
        self.base_directory = base_directory
        self.folders_created: List[str] = []

    def organize_files(self, files: List[FileHandler]) -> Dict[str, int]:
        files_by_type = self._group_files_by_type(files)

        files_by_type.pop("Imagem", None)

        moved_files = {}

        for file_type, file_list in files_by_type.items():
            if file_list:  # Só cria pasta se houver arquivos do tipo
                folder_name = self._get_folder_name(file_type)
                target_folder = self.base_directory / folder_name

                self._create_folder_if_needed(target_folder)

                moved_count = self._move_files(file_list, target_folder)
                moved_files[file_type] = moved_count

        return moved_files

    def _group_files_by_type(
        self, files: List[FileHandler]
    ) -> Dict[str, List[FileHandler]]:

        grouped: Dict[str, List[FileHandler]] = {}
        for file in files:
            if file.type not in grouped:
                grouped[file.type] = []
            grouped[file.type].append(file)
        return grouped

    def _get_folder_name(self, file_type: str) -> str:

        folder_mapping = {"Vídeo": "Videos", "Texto": "Textos", "Outro": "Outros"}
        return folder_mapping.get(file_type, "Outros")

    def _create_folder_if_needed(self, folder_path: Path) -> None:
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            self.folders_created.append(folder_path.name)
            print(f"Pasta criada: {folder_path.name}")

    def _move_files(self, files: List[FileHandler], target_folder: Path) -> int:
        moved_count = 0
        for file in files:
            try:
                target_path = target_folder / file.name

                if target_path.exists():
                    print(f"Aviso: Arquivo já existe no destino, pulando: {file.name}")
                    continue

                shutil.move(str(file.path), str(target_path))
                moved_count += 1
                print(f"Movido: {file.name} -> {target_folder.name}/")

            except (OSError, shutil.Error) as e:
                print(f"Erro ao mover {file.name}: {e}")

        return moved_count

    def get_organization_summary(
        self, moved_files: Dict[str, int], total_files: int
    ) -> str:
        summary = ["\n=== RESUMO DA ORGANIZAÇÃO ==="]

        if self.folders_created:
            summary.append(f"Pastas criadas: {', '.join(self.folders_created)}")
        else:
            summary.append("Nenhuma pasta nova foi criada.")

        summary.append(f"Total de arquivos analisados: {total_files}")

        if moved_files:
            summary.append("Arquivos movidos:")
            for file_type, count in moved_files.items():
                folder_name = self._get_folder_name(file_type)
                summary.append(
                    f"  • {count} arquivo(s) de {file_type} -> {folder_name}/"
                )
        else:
            summary.append("Nenhum arquivo foi movido.")

        images_count = (
            total_files - sum(moved_files.values()) if moved_files else total_files
        )
        if images_count > 0:
            summary.append(
                f"  • {images_count} imagem(ns) permaneceu(ram) na pasta atual"
            )

        return "\n".join(summary)
