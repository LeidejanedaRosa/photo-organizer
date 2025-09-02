import os
import shutil
from typing import Dict, List
from collections import defaultdict

from ..domain.image import ImageInfo
from ..utils.ui_formatter import UIFormatter
from ..utils.file_manager import FileManager


class DuplicateManager:
    
    def __init__(self):
        self.ui_formatter = UIFormatter()
        self.file_manager = FileManager()
    
    def find_duplicates(self, images: List[ImageInfo]) -> Dict[str, List[ImageInfo]]:
        
        grupos_hash: Dict[str, List[ImageInfo]] = defaultdict(list)
        
        for img in images:
            if img.hash_imagem:
                grupos_hash[img.hash_imagem].append(img)
        
        return {
            hash_: grupo
            for hash_, grupo in grupos_hash.items()
            if len(grupo) > 1
        }
    
    def move_duplicates(
        self,
        duplicadas: Dict[str, List[ImageInfo]],
        diretorio_origem: str,
        simular: bool = True
    ) -> int:
        
        if not self.ui_formatter.validate_list_not_empty(
            duplicadas, "Nenhuma imagem duplicada encontrada!"
        ):
            return 0
        
        pasta_duplicadas = os.path.join(diretorio_origem, "duplicadas")
        
        self.ui_formatter.print_operation_header("Movendo duplicatas", simular)
        self.ui_formatter.print_separator()
        
        total_moved = 0
        total_grupos = len(duplicadas)
        
        for i, grupo in enumerate(duplicadas.values(), 1):
            original = grupo[0]
            
            print(f"\n📂 Grupo {i}/{total_grupos} de duplicatas:")
            print(f"   🏠 Mantendo: {original.file}")
            
            for duplicate in grupo[1:]:
                origem = os.path.join(diretorio_origem, duplicate.file)
                destino = os.path.join(pasta_duplicadas, duplicate.file)
                
                if not simular:
                    self.file_manager.create_directory_if_not_exists(
                        pasta_duplicadas, "duplicadas"
                    )
                
                if self.file_manager.move_single_file(
                    origem, destino, duplicate.file, simular
                ):
                    if not simular:
                        total_moved += 1
                else:
                    total_moved += 1 if simular else 0
        
        self.ui_formatter.print_operation_result(
            "Movimentação de duplicatas",
            total_moved,
            "imagens",
            simular
        )
        
        return total_moved
