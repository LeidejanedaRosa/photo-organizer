from pathlib import Path


class FileHandler:
    """
    Representa e manipula um único arquivo no sistema de arquivos.

    Esta classe encapsula as informações e operações relacionadas a um arquivo,
    como obter seu tipo com base na extensão.
    """

    def __init__(self, file_path: Path):
        """
        Inicializa o FileHandler.

        Args:
            file_path (Path): O caminho para o arquivo.
        """
        if not file_path.is_file():
            raise ValueError(f"O caminho fornecido não é um arquivo: {file_path}")
        self.path = file_path
        self.name = file_path.name
        self.extension = file_path.suffix
        self.type = self._get_file_type()

    def _get_file_type(self) -> str:
        """
        Retorna o tipo de arquivo com base na extensão.

        Returns:
            str: O tipo do arquivo (Imagem, Vídeo, Texto, Outro).
        """
        image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}
        video_extensions = {".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"}
        text_extensions = {".txt", ".doc", ".docx", ".pdf", ".rtf", ".odt"}

        if self.extension.lower() in image_extensions:
            return "Imagem"
        if self.extension.lower() in video_extensions:
            return "Vídeo"
        if self.extension.lower() in text_extensions:
            return "Texto"
        return "Outro"

    def __str__(self) -> str:
        return f"Arquivo: {self.name} - Tipo: {self.type}"
