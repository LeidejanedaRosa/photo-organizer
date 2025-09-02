from abc import ABC, abstractmethod
from typing import Any, Dict, List

from ..domain.image import ImageInfo
from ..utils.file_manager import FileManager
from ..utils.ui_formatter import UIFormatter


class BaseOrganizer(ABC):

    def __init__(self):
        self.ui_formatter = UIFormatter()
        self.file_manager = FileManager()

    @abstractmethod
    def _group_images(
        self, images: List[ImageInfo]
    ) -> Dict[str, List[ImageInfo]]:

        pass

    @abstractmethod
    def _get_operation_name(self) -> str:

        pass

    @abstractmethod
    def _get_empty_message(self) -> str:

        pass

    def organize(
        self, images: List[ImageInfo], directory: str, simular: bool = True
    ) -> Any:

        if not self.ui_formatter.validate_list_not_empty(
            images, self._get_empty_message()
        ):
            return {}

        grouped_images = self._group_images(images)

        if not grouped_images:
            print(f"📅 {self._get_empty_message()}")
            return {}

        self.ui_formatter.print_operation_header(
            self._get_operation_name(), simular
        )
        self.ui_formatter.print_separator()

        total_processed = 0
        result = {}

        for group_name, group_images in grouped_images.items():
            result[group_name] = group_images
            total_processed += self._process_group(
                group_name, group_images, directory, simular
            )

        self.ui_formatter.print_operation_result(
            self._get_operation_name(), total_processed, "imagens", simular
        )

        return result

    def _process_group(
        self,
        group_name: str,
        images: List[ImageInfo],
        directory: str,
        simular: bool,
    ) -> int:

        self.ui_formatter.print_group_header(
            group_name, len(images), "imagem(ns)"
        )

        target_directory = self._get_target_directory(directory, group_name)

        if not simular:
            self.file_manager.create_directory_if_not_exists(
                target_directory, group_name
            )
        else:
            print(f"   📁 Criaria pasta: {group_name}/")

        return self.file_manager.move_files_to_directory(
            images, directory, target_directory, simular
        )

    def _get_target_directory(
        self, base_directory: str, group_name: str
    ) -> str:

        import os

        return os.path.join(base_directory, group_name)
