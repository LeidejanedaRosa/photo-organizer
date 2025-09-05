from typing import Any, Dict

from .models import OrganizationRequest, OrganizationResult
from .service import PhotoOrganizerService


class PhotoOrganizerController:

    def __init__(self):
        self.service = PhotoOrganizerService()

    def analyze_folder_endpoint(self, folder_path: str) -> Dict[str, Any]:
        result = self.service.analyze_folder(folder_path)

        return {
            "success": result.success,
            "message": result.message,
            "data": {
                "source_folder": result.source_folder,
                "total_files": result.total_files,
                "files_by_type": result.files_by_type,
                "files": [
                    {
                        "name": file.name,
                        "path": file.path,
                        "extension": file.extension,
                        "type": file.file_type,
                        "size": file.size,
                    }
                    for file in result.files_found
                ],
            },
            "errors": result.errors,
        }

    def organize_files_endpoint(
        self, folder_path: str, organize: bool = True
    ) -> Dict[str, Any]:
        request = OrganizationRequest(source_folder=folder_path, organize=organize)

        result = self.service.organize_files(request)

        response_data = {
            "source_folder": request.source_folder,
            "total_files": result.total_files,
            "files_by_type": result.files_by_type,
            "files": [
                {
                    "name": file.name,
                    "path": file.path,
                    "extension": file.extension,
                    "type": file.file_type,
                    "size": file.size,
                }
                for file in result.files_found
            ],
        }

        if organize:
            response_data.update(
                {
                    "moved_files": result.moved_files,
                    "folders_created": result.folders_created,
                    "organization_summary": self._generate_summary(result),
                }
            )

        return {
            "success": result.success,
            "message": result.message,
            "data": response_data,
            "errors": result.errors,
        }

    def get_supported_file_types_endpoint(self) -> Dict[str, Any]:
        return {
            "success": True,
            "message": "Tipos de arquivo suportados",
            "data": {
                "image_extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
                "video_extensions": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
                "text_extensions": [".txt", ".doc", ".docx", ".pdf", ".rtf", ".odt"],
                "folder_mapping": {
                    "Imagem": "Permanecem na pasta atual",
                    "Vídeo": "Videos/",
                    "Texto": "Textos/",
                    "Outro": "Outros/",
                },
            },
            "errors": [],
        }

    def _generate_summary(self, result: OrganizationResult) -> Dict[str, Any]:
        total_moved = sum(result.moved_files.values())
        files_remaining = result.total_files - total_moved

        return {
            "total_analyzed": result.total_files,
            "total_moved": total_moved,
            "files_remaining": files_remaining,
            "folders_created": result.folders_created,
            "moved_by_type": result.moved_files,
        }
