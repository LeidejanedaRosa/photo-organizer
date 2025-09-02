import os
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from ..domain.configuration import ProjectConfiguration
from ..domain.image import ImageInfo
from ..utils.base_organizer import BaseOrganizer
from ..utils.file_manager import FileManager
from ..utils.ui_formatter import UIFormatter


class YearOrganizer(BaseOrganizer):

    def _group_images(
        self, images: List[ImageInfo]
    ) -> Dict[str, List[ImageInfo]]:

        images_by_year = defaultdict(list)

        for img in images:
            year = img.preferred_date.year
            images_by_year[f"Ano {year}"].append(img)

        return dict(images_by_year)

    def _get_operation_name(self) -> str:
        return "Organizando por anos"

    def _get_empty_message(self) -> str:
        return "Nenhuma imagem com data válida para organização por anos."


class EventOrganizer:

    def __init__(self):
        self.ui_formatter = UIFormatter()
        self.file_manager = FileManager()

    def organize_by_events(
        self,
        directory: str,
        detected_events: Dict[str, List[str]],
        simulate: bool = True,
    ) -> int:

        if not detected_events:
            print("📋 Nenhum evento detectado nos nomes dos arquivos.")
            return 0

        self.ui_formatter.print_operation_header(
            "Organizando por eventos", simulate
        )
        self.ui_formatter.print_separator()

        total_moved = 0

        for event, files in detected_events.items():
            event_folder = os.path.join(directory, event)

            self.ui_formatter.print_group_header(
                event, len(files), "arquivo(s)"
            )

            if not simulate:
                self.file_manager.create_directory_if_not_exists(
                    event_folder, event
                )
            else:
                print(f"   📁 Criaria pasta: {event}/")

            for file in files:
                source = os.path.join(directory, file)
                destination = os.path.join(event_folder, file)

                if self.file_manager.move_single_file(
                    source, destination, file, simulate
                ):
                    if not simulate:
                        total_moved += 1
                else:
                    total_moved += 1 if simulate else 0

        self.ui_formatter.print_operation_result(
            "Organização por eventos", total_moved, "arquivos", simulate
        )

        return total_moved


class FolderOrganizer:

    def __init__(self):
        self.year_organizer = YearOrganizer()
        self.event_organizer = EventOrganizer()
        self.ui_formatter = UIFormatter()
        self.file_manager = FileManager()

    def organize_by_years(
        self, images: List[ImageInfo], directory: str, simulate: bool = True
    ) -> Dict[int, List[ImageInfo]]:

        result = self.year_organizer.organize(images, directory, simulate)

        converted_result = {}
        for key, value in result.items():
            year = int(key.replace("Ano ", ""))
            converted_result[year] = value

        return converted_result

    def organize_by_events(
        self,
        directory: str,
        detected_events: Dict[str, List[str]],
        simulate: bool = True,
    ) -> int:

        return self.event_organizer.organize_by_events(
            directory, detected_events, simulate
        )

    def detect_events_in_files(
        self, images: List[ImageInfo]
    ) -> Dict[str, List[str]]:

        events = defaultdict(list)

        for img in images:
            filename = Path(img.file).stem

            if " - " in filename:
                parts = filename.split(" - ")
                if len(parts) >= 2:
                    event_part = " - ".join(parts[1:])
                    if event_part and not event_part.isdigit():
                        events[event_part].append(img.file)

        return dict(events)

    def organize_by_custom_periods(
        self,
        images: List[ImageInfo],
        directory: str,
        configuration: ProjectConfiguration,
        simulate: bool = True,
    ) -> Dict[str, List[ImageInfo]]:

        if not self.ui_formatter.validate_list_not_empty(
            images, "Nenhuma imagem para organizar por períodos."
        ):
            return {}

        current_period_images = []
        future_period_images = []

        for img in images:
            period_number = configuration.calculate_period_number(
                img.preferred_date
            )
            if period_number == configuration.calculate_period_number(
                configuration.start_date
            ):
                current_period_images.append(img)
            else:
                future_period_images.append(img)

        self.ui_formatter.print_operation_header(
            "Organizando por períodos customizados", simulate
        )
        self.ui_formatter.print_separator()

        result = {}

        if current_period_images:
            current_folder_name = self._generate_period_folder_name(
                configuration
            )
            result[current_folder_name] = current_period_images

            if not simulate:
                self._create_folder_and_move(
                    current_period_images, directory, current_folder_name
                )

            print(
                f"📁 {current_folder_name}: {len(current_period_images)} imagens"
            )

        if future_period_images:
            new_config = configuration.suggest_new_period_config()
            if new_config:
                future_folder_name = self._generate_period_folder_name(
                    new_config
                )
                result[future_folder_name] = future_period_images

                if not simulate:
                    self._create_folder_and_move(
                        future_period_images, directory, future_folder_name
                    )

                print(
                    f"📁 {future_folder_name}: {len(future_period_images)} imagens"
                )

        self.ui_formatter.print_separator()
        return result

    def _generate_period_folder_name(
        self, config: ProjectConfiguration
    ) -> str:

        components = []

        if config.include_period:
            period_num = config.calculate_period_number(config.start_date)
            components.append(f"{period_num:02d}")

        components.append(config.naming_prefix)

        date_str = config.start_date.strftime(config.date_format)
        components.append(date_str)

        name = config.separator.join(components)

        return name

    def _create_folder_and_move(
        self, images: List[ImageInfo], base_directory: str, folder_name: str
    ) -> None:

        destination_folder = os.path.join(base_directory, folder_name)

        self.file_manager.create_directory_if_not_exists(
            destination_folder, folder_name
        )

        for img in images:
            source = os.path.join(base_directory, img.file)
            destination = os.path.join(destination_folder, img.file)

            try:
                shutil.move(source, destination)
                img.file = os.path.join(
                    folder_name, os.path.basename(img.file)
                )
                print(f"   📤 Movida: {img.file}")
            except (IOError, OSError) as e:
                print(f"   ❌ Erro ao mover {img.file}: {e}")
