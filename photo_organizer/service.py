from pathlib import Path
from typing import Dict, List

from .directory_scanner import DirectoryScanner
from .file_handler import FileHandler
from .file_organizer import FileOrganizer
from .models import AnalysisResult, FileInfo, OrganizationRequest, OrganizationResult


class PhotoOrganizerService:

    def _convert_to_file_info(self, files: List[FileHandler]) -> List[FileInfo]:
        files_info = []
        for file in files:
            try:
                size = file.path.stat().st_size if file.path.exists() else 0
                files_info.append(
                    FileInfo(
                        name=file.name,
                        path=str(file.path),
                        extension=file.extension,
                        file_type=file.type,
                        size=size,
                    )
                )
            except (OSError, AttributeError):
                files_info.append(
                    FileInfo(
                        name=file.name,
                        path=str(file.path),
                        extension=file.extension,
                        file_type=file.type,
                        size=0,
                    )
                )
        return files_info

    def _group_files_count_by_type(self, files: List[FileHandler]) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for file in files:
            counts[file.type] = counts.get(file.type, 0) + 1
        return counts

    def analyze_folder(self, folder_path: str) -> AnalysisResult:
        try:
            source_path = Path(folder_path).expanduser().resolve()
            if not source_path.exists():
                return AnalysisResult(
                    success=False,
                    message=f"Pasta não encontrada: {source_path}",
                    total_files=0,
                    files_by_type={},
                    files_found=[],
                    source_folder=str(source_path),
                    errors=[f"Pasta não encontrada: {source_path}"],
                )

            if not source_path.is_dir():
                return AnalysisResult(
                    success=False,
                    message=f"Caminho não é uma pasta: {source_path}",
                    total_files=0,
                    files_by_type={},
                    files_found=[],
                    source_folder=str(source_path),
                    errors=[f"Caminho não é uma pasta: {source_path}"],
                )

            scanner = DirectoryScanner(source_path)
            files = scanner.scan_files()

            files_info = self._convert_to_file_info(files)

            files_by_type = self._group_files_count_by_type(files)

            return AnalysisResult(
                success=True,
                message=f"Análise concluída. {len(files)} arquivo(s) encontrado(s).",
                total_files=len(files),
                files_by_type=files_by_type,
                files_found=files_info,
                source_folder=str(source_path),
                errors=[],
            )

        except (OSError, ValueError) as e:
            return AnalysisResult(
                success=False,
                message=f"Erro durante análise: {str(e)}",
                total_files=0,
                files_by_type={},
                files_found=[],
                source_folder=folder_path,
                errors=[str(e)],
            )

    def organize_files(self, request: OrganizationRequest) -> OrganizationResult:

        try:
            analysis = self.analyze_folder(request.source_folder)
            if not analysis.success:
                return OrganizationResult(
                    success=False,
                    message=analysis.message,
                    total_files=0,
                    files_by_type={},
                    moved_files={},
                    folders_created=[],
                    files_found=[],
                    errors=analysis.errors,
                )

            source_path = Path(request.source_folder).expanduser().resolve()

            if not request.organize:
                return OrganizationResult(
                    success=True,
                    message="Análise concluída. Use organize=True para organizar os arquivos.",
                    total_files=analysis.total_files,
                    files_by_type=analysis.files_by_type,
                    moved_files={},
                    folders_created=[],
                    files_found=analysis.files_found,
                    errors=[],
                )

            scanner = DirectoryScanner(source_path)
            files = scanner.scan_files()

            organizer = FileOrganizer(source_path)
            moved_files = organizer.organize_files(files)

            files_info = self._convert_to_file_info(files)

            return OrganizationResult(
                success=True,
                message=f"Organização concluída! {sum(moved_files.values())} arquivo(s) movido(s).",
                total_files=len(files),
                files_by_type=analysis.files_by_type,
                moved_files=moved_files,
                folders_created=organizer.folders_created,
                files_found=files_info,
                errors=[],
            )

        except (OSError, ValueError) as e:
            return OrganizationResult(
                success=False,
                message=f"Erro durante organização: {str(e)}",
                total_files=0,
                files_by_type={},
                moved_files={},
                folders_created=[],
                files_found=[],
                errors=[str(e)],
            )
