"""
Este módulo foi refatorado e sua funcionalidade foi distribuída em:
- ImageAnalyzer: para análise de imagens
- DuplicateManager: para gerenciamento de duplicatas
- FilenameGenerator: para geração de nomes

Mantido apenas para compatibilidade com versões anteriores.
"""

from .image_analyzer import ImageAnalyzer
from .duplicate_manager import DuplicateManager
from .file_renamer import FilenameGenerator


class ImageProcessor:
    """Classe mantida para compatibilidade. Use os novos serviços específicos."""
    
    def __init__(self):
        self.analyzer = ImageAnalyzer()
        self.duplicate_manager = DuplicateManager()
        self.filename_generator = FilenameGenerator()
    
    def calculate_image_hash(self, image_path):
        """Usa o ImageAnalyzer para calcular hash."""
        return self.analyzer._calculate_image_hash(image_path)
    
    def is_duplicate_image(self, hash1, hash2):
        """Verifica se duas imagens são duplicadas."""
        return hash1 == hash2
    
    def generate_new_filename(self, base_name, extension):
        """Gera nome único para arquivo."""
        import os
        counter = 1
        new_name = f"{base_name}{extension}"
        
        while os.path.exists(new_name):
            counter += 1
            new_name = f"{base_name}_{counter}{extension}"
            
        return new_name
