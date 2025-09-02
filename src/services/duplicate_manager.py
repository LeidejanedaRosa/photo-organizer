import os
import shutil
from typing import Dict, List
from collections import defaultdict

from ..domain.image import ImageInfo

class DuplicateManager:
    
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
        
        if not duplicadas:
            print("✅ Nenhuma imagem duplicada encontrada!")
            return 0
        
        pasta_duplicadas = os.path.join(diretorio_origem, "duplicadas")
        if not simular and not os.path.exists(pasta_duplicadas):
            os.makedirs(pasta_duplicadas)
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Movendo duplicatas...")
        else:
            print("\n📦 MOVENDO DUPLICATAS...")
        
        print("─" * 60)
        
        total_movidas = 0
        total_grupos = len(duplicadas)
        
        for i, grupo in enumerate(duplicadas.values(), 1):
            original = grupo[0]
            print(f"\n📂 Grupo {i}/{total_grupos} de duplicatas:")
            print(f"   🏠 Mantendo: {original.file}")
            
            for duplicate in grupo[1:]:
                origem = os.path.join(diretorio_origem, duplicate.file)
                destino = os.path.join(pasta_duplicadas, duplicate.file)
                
                if simular:
                    print(f"   📤 Moveria: {duplicate.file}")
                else:
                    print(f"   📤 Movendo: {duplicate.file}")
                    try:
                        shutil.move(origem, destino)
                        total_movidas += 1
                        print("      ✅ Sucesso")
                    except (IOError, OSError) as e:
                        print(f"      ❌ Erro: {e}")
        
        print("─" * 60)
        if not simular:
            print(f"📊 RESULTADO: {total_movidas} images moved para 'duplicadas/'")
        else:
            duplicatas_total = sum(len(grupo) - 1 for grupo in duplicadas.values())
            print(f"📊 PREVISÃO: {duplicatas_total} images seriam moved")
        print("─" * 60)
        
        return total_movidas