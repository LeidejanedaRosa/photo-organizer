import os
import shutil
from typing import List
from ..domain.image import ImageInfo


class FileManager:
    
    @staticmethod
    def create_directory_if_not_exists(directory_path: str, display_name: str = None) -> bool:
        
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            folder_name = display_name or os.path.basename(directory_path)
            print(f"   ✅ Pasta criada: {folder_name}/")
            return True
        return False
    
    @staticmethod
    def move_files_to_directory(
        images: List[ImageInfo],
        source_directory: str,
        target_directory: str,
        simular: bool = True
    ) -> int:
        
        moved_count = 0
        
        for img in images:
            source_path = os.path.join(source_directory, img.file)
            target_path = os.path.join(target_directory, img.file)
            
            if simular:
                print(f"   📤 Moveria: {img.file}")
            else:
                print(f"   📤 Movendo: {img.file}")
                try:
                    shutil.move(source_path, target_path)
                    moved_count += 1
                    print("      ✅ Sucesso")
                except (IOError, OSError) as e:
                    print(f"      ❌ Erro: {e}")
        
        return moved_count if not simular else len(images)
    
    @staticmethod
    def move_single_file(
        source_path: str,
        target_path: str,
        filename: str,
        simular: bool = True
    ) -> bool:
        
        if simular:
            print(f"   📤 Moveria: {filename}")
            return True
        else:
            print(f"   📤 Movendo: {filename}")
            try:
                shutil.move(source_path, target_path)
                print("      ✅ Sucesso")
                return True
            except (IOError, OSError) as e:
                print(f"      ❌ Erro: {e}")
                return False
