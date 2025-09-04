from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class FileInfo:
    name: str
    path: str
    extension: str
    file_type: str
    size: int


@dataclass
class OrganizationRequest:
    source_folder: str
    organize: bool = False
    create_folders: Optional[List[str]] = None


@dataclass
class OrganizationResult:
    success: bool
    message: str
    total_files: int
    files_by_type: Dict[str, int]
    moved_files: Dict[str, int]
    folders_created: List[str]
    files_found: List[FileInfo]
    errors: List[str]


@dataclass
class AnalysisResult:
    success: bool
    message: str
    total_files: int
    files_by_type: Dict[str, int]
    files_found: List[FileInfo]
    source_folder: str
    errors: List[str]
