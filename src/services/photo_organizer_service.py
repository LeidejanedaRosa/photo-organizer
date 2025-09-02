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

        imagens_organizadas = []
        imagens_nao_organizadas = []

        for img in all_images:
            if self.filename_generator.is_organized(img.file):
                imagens_organizadas.append(img)
            else:
                imagens_nao_organizadas.append(img)

        def sort_by_date(x):
            return x.preferred_date

        imagens_organizadas.sort(key=sort_by_date)
        imagens_nao_organizadas.sort(key=sort_by_date)

        return imagens_nao_organizadas, imagens_organizadas

    def detect_and_move_duplicates(
        self, images: List[ImageInfo], directory: str, simular: bool = True
    ) -> int:

        return self.operation_manager.execute_with_backup(
            self._execute_duplicate_detection,
            directory,
            "mover_duplicatas",
            bool(images),
            images,
            directory,
            simular=simular,
        )

    def _execute_duplicate_detection(
        self, images: List[ImageInfo], directory: str, simular: bool = True
    ) -> int:

        duplicadas = self.duplicate_manager.find_duplicates(images)
        return self.duplicate_manager.move_duplicates(
            duplicadas, directory, simular
        )

    def rename_images(
        self,
        images: List[ImageInfo],
        directory: str,
        events: Optional[Dict[str, str]] = None,
        simular: bool = True,
    ) -> int:

        return self.operation_manager.execute_with_backup(
            self.file_renamer.rename_images,
            directory,
            "renomear_imagens",
            bool(images),
            images,
            directory,
            events,
            simular=simular,
        )

    def organize_by_years(
        self, images: List[ImageInfo], directory: str, simular: bool = True
    ) -> Dict[int, List[ImageInfo]]:

        return self.operation_manager.execute_with_backup(
            self.folder_organizer.organize_by_years,
            directory,
            "organizar_anos",
            bool(images),
            images,
            directory,
            simular=simular,
        )

    def organize_by_events(
        self, images: List[ImageInfo], directory: str, simular: bool = True
    ) -> int:

        eventos_detectados = self.folder_organizer.detect_events_in_files(
            images
        )

        return self.operation_manager.execute_with_backup(
            self._execute_organize_by_events,
            directory,
            "organizar_eventos",
            bool(eventos_detectados),
            directory,
            eventos_detectados,
            simular=simular,
        )

    def _execute_organize_by_events(
        self, directory: str, eventos_detectados: Dict, simular: bool = True
    ) -> int:

        return self.folder_organizer.organize_by_events(
            directory, eventos_detectados, simular
        )

    def organize_by_custom_periods(
        self,
        images: List[ImageInfo],
        directory: str,
        configuration: "ProjectConfiguration",
        simular: bool = True,
    ) -> Dict[str, List[ImageInfo]]:

        if not simular and images:
            backup_file = self.backup_manager.create_backup(
                directory, "organizar_periodos"
            )
            print(f"💾 Backup criado: {backup_file}")

        return self.folder_organizer.organize_by_custom_periods(
            images, directory, configuration, simular
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
        imagens_nao_organizadas: List[ImageInfo],
        imagens_organizadas: List[ImageInfo],
    ) -> None:

        total_imagens = len(imagens_nao_organizadas) + len(imagens_organizadas)

        print("\n📊 ESTATÍSTICAS:")
        print(f"Total de images encontradas: {total_imagens}")
        print(f"Já organizadas: {len(imagens_organizadas)}")
        print(f"Precisam ser organizadas: {len(imagens_nao_organizadas)}")

        if imagens_organizadas:
            print(f"\n✅ IMAGENS JÁ ORGANIZADAS ({len(imagens_organizadas)}):")
            for img in imagens_organizadas:
                print(f"  - {img.file}")

        if not imagens_nao_organizadas:
            print("\n🎉 Todas as images já estão organizadas!")
            return

        print(f"\n📋 IMAGENS PARA ORGANIZAR ({len(imagens_nao_organizadas)}):")
        self._print_image_details(imagens_nao_organizadas)

    def _print_image_details(self, images: List[ImageInfo]) -> None:

        for img in images:
            print(f"Arquivo: {img.file}")
            print(f"Formato: {img.formato}")
            print(f"Dimensões: {img.dimensions}")
            print(f"Modo: {img.modo}")
            print(f"Tamanho (bytes): {img.tamanho}")
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
