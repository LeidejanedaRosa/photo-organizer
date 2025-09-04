from pathlib import Path
from typing import List

from .file_handler import FileHandler


class DirectoryScanner:
    """
    Responsável por escanear um diretório e encontrar arquivos.

    Esta classe segue o Princípio da Responsabilidade Única (SRP),
    focando apenas em percorrer um diretório e criar instâncias
    de FileHandler para cada arquivo encontrado.
    """

    def __init__(self, directory_path: Path):
        """
        Inicializa o DirectoryScanner.

        Args:
            directory_path (Path): O caminho para o diretório a ser escaneado.
        """
        if not directory_path.is_dir():
            raise ValueError(
                f"O caminho fornecido não é um diretório: {directory_path}"
            )
        self.directory_path = directory_path

    def scan_files(self) -> List[FileHandler]:
        """
        Escaneia o diretório em busca de arquivos.

        Returns:
            List[FileHandler]: Uma lista de objetos FileHandler
                               representando os arquivos encontrados.
        """
        files = [
            FileHandler(file_path)
            for file_path in self.directory_path.iterdir()
            if file_path.is_file()
        ]
        return files
