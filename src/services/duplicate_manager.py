import os
from collections import defaultdict
from typing import Dict, List

from ..domain.image import ImageInfo
from ..utils.file_manager import FileManager
from ..utils.ui_formatter import UIFormatter


class DuplicateManager:

    def __init__(self):
        self.ui_formatter = UIFormatter()
        self.file_manager = FileManager()

    def find_duplicates(
        self, images: List[ImageInfo]
    ) -> Dict[str, List[ImageInfo]]:

        groups_hash: Dict[str, List[ImageInfo]] = defaultdict(list)

        for img in images:
            if img.hash_image:
                groups_hash[img.hash_image].append(img)

        return {
            hash_: group
            for hash_, group in groups_hash.items()
            if len(group) > 1
        }

    def move_duplicates(
        self,
        duplicates: Dict[str, List[ImageInfo]],
        origin_directory: str,
        simulate: bool = True,
    ) -> int:

        if not self.ui_formatter.validate_list_not_empty(
            duplicates, "Nenhuma imagem duplicada encontrada!"
        ):
            return 0

        duplicate_folders = os.path.join(origin_directory, "duplicadas")

        self.ui_formatter.print_operation_header(
            "Movendo duplicatas", simulate
        )
        self.ui_formatter.print_separator()

        total_moved = 0
        total_groups = len(duplicates)

        for i, groups in enumerate(duplicates.values(), 1):
            original = groups[0]

            print(f"\n📂 Grupo {i}/{total_groups} de duplicatas:")
            print(f"   🏠 Mantendo: {original.file}")

            for duplicate in groups[1:]:
                origin = os.path.join(origin_directory, duplicate.file)
                destination = os.path.join(duplicate_folders, duplicate.file)

                if not simulate:
                    self.file_manager.create_directory_if_not_exists(
                        duplicate_folders, "duplicadas"
                    )

                if self.file_manager.move_single_file(
                    origin, destination, duplicate.file, simulate
                ):
                    if not simulate:
                        total_moved += 1
                else:
                    total_moved += 1 if simulate else 0

        self.ui_formatter.print_operation_result(
            "Movimentação de duplicatas", total_moved, "imagens", simulate
        )

        return total_moved
