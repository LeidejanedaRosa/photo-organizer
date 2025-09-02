from typing import Dict, List, Optional

from ..domain.configuration import ProjectConfiguration
from ..domain.image import ImageInfo
from ..utils.operation_manager import OperationManager
from .backup_manager import BackupManager
from .duplicate_manager import DuplicateManager
from .file_renamer import FilenameGenerator, FileRenamer
from .folder_organizer import FolderOrganizer
from .image_analyzer import ImageAnalyzer
from .report_generator import ReportGenerator


class PhotoOrganizerService:

    def __init__(self, configuration: Optional[ProjectConfiguration] = None):
        self.configuration = configuration
        self.image_analyzer = ImageAnalyzer()
        self.duplicate_manager = DuplicateManager()
        self.file_renamer = FileRenamer()
        self.folder_organizer = FolderOrganizer()
        self.backup_manager = BackupManager()
        self.report_generator = ReportGenerator()
        self.filename_generator = FilenameGenerator(configuration)
        self.operation_manager = OperationManager(self.backup_manager)

    def set_configuration(self, configuration: ProjectConfiguration) -> None:

        self.configuration = configuration
        self.filename_generator = FilenameGenerator(configuration)

    def analyze_directory(
        self, directory: str
    ) -> tuple[List[ImageInfo], List[ImageInfo]]:

        all_images = self.image_analyzer.analyze_directory(directory)

        organized_images = []
        unorganized_images = []

        for img in all_images:
            if self.filename_generator.is_organized(img.file):
                organized_images.append(img)
            else:
                unorganized_images.append(img)

        def sort_by_date(x):
            return x.preferred_date

        organized_images.sort(key=sort_by_date)
        unorganized_images.sort(key=sort_by_date)

        return unorganized_images, organized_images

    def detect_and_move_duplicates(
        self, images: List[ImageInfo], directory: str, simulate: bool = True
    ) -> int:

        return self.operation_manager.execute_with_backup(
            self._execute_duplicate_detection,
            directory,
            "mover_duplicatas",
            bool(images),
            images,
            directory,
            simulate=simulate,
        )

    def _execute_duplicate_detection(
        self, images: List[ImageInfo], directory: str, simulate: bool = True
    ) -> int:

        duplicates = self.duplicate_manager.find_duplicates(images)
        return self.duplicate_manager.move_duplicates(
            duplicates, directory, simulate
        )

    def rename_images(
        self,
        images: List[ImageInfo],
        directory: str,
        events: Optional[Dict[str, str]] = None,
        simulate: bool = True,
    ) -> int:

        return self.operation_manager.execute_with_backup(
            self.file_renamer.rename_images,
            directory,
            "renomear_imagens",
            bool(images),
            images,
            directory,
            events,
            simulate=simulate,
        )

    def organize_by_years(
        self, images: List[ImageInfo], directory: str, simulate: bool = True
    ) -> Dict[int, List[ImageInfo]]:

        return self.operation_manager.execute_with_backup(
            self.folder_organizer.organize_by_years,
            directory,
            "organizar_anos",
            bool(images),
            images,
            directory,
            simulate=simulate,
        )

    def organize_by_events(
        self, images: List[ImageInfo], directory: str, simulate: bool = True
    ) -> int:

        detected_events = self.folder_organizer.detect_events_in_files(images)

        return self.operation_manager.execute_with_backup(
            self._execute_organize_by_events,
            directory,
            "organizar_eventos",
            bool(detected_events),
            directory,
            detected_events,
            simulate=simulate,
        )

    def _execute_organize_by_events(
        self, directory: str, detected_events: Dict, simulate: bool = True
    ) -> int:

        return self.folder_organizer.organize_by_events(
            directory, detected_events, simulate
        )

    def organize_by_custom_periods(
        self,
        images: List[ImageInfo],
        directory: str,
        configuration: "ProjectConfiguration",
        simulate: bool = True,
    ) -> Dict[str, List[ImageInfo]]:

        if not simulate and images:
            backup_file = self.backup_manager.create_backup(
                directory, "organizar_periodos"
            )
            print(f"💾 Backup criado: {backup_file}")

        return self.folder_organizer.organize_by_custom_periods(
            images, directory, configuration, simulate
        )

    def generate_report(self, images: List[ImageInfo]) -> None:

        self.report_generator.generate_detailed_report(images)

    def search_photos_by_period(
        self, images: List[ImageInfo], start_date: str, end_date: str
    ) -> List[ImageInfo]:

        return self.report_generator.search_photos_by_period(
            images, start_date, end_date
        )

    def create_manual_backup(self, directory: str) -> str:

        return self.backup_manager.create_backup(directory, "backup_manual")

    def print_analysis_statistics(
        self,
        unorganized_images: List[ImageInfo],
        organized_images: List[ImageInfo],
    ) -> None:

        total_images = len(unorganized_images) + len(organized_images)

        print("\n📊 ESTATÍSTICAS:")
        print(f"Total de images encontradas: {total_images}")
        print(f"Já organizadas: {len(organized_images)}")
        print(f"Precisam ser organizadas: {len(unorganized_images)}")

        if organized_images:
            print(f"\n✅ IMAGENS JÁ ORGANIZADAS ({len(organized_images)}):")
            for img in organized_images:
                print(f"  - {img.file}")

        if not unorganized_images:
            print("\n🎉 Todas as images já estão organizadas!")
            return

        print(f"\n📋 IMAGENS PARA ORGANIZAR ({len(unorganized_images)}):")
        self._print_image_details(unorganized_images)

    def _print_image_details(self, images: List[ImageInfo]) -> None:

        for img in images:
            print(f"Arquivo: {img.file}")
            print(f"Formato: {img.format}")
            print(f"Dimensões: {img.dimensions}")
            print(f"Modo: {img.mode}")
            print(f"Tamanho (bytes): {img.size}")
            print(
                f"Data de modificação: "
                f"{img.data_mod.strftime('%d/%m/%Y %H:%M:%S')}"
            )
            if img.data_exif:
                print(
                    f"Data EXIF: "
                    f"{img.data_exif.strftime('%d/%m/%Y %H:%M:%S')}"
                )
            print("-" * 40)
