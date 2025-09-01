import re
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

from ..domain.image import ImageInfo, BabyAge, Event


class FilenameGenerator:
    """Responsável por gerar nomes de arquivos seguindo o padrão estabelecido."""
    
    def generate_filename(
        self,
        info: ImageInfo,
        numero_sequencial: int = 0,
        eventos: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Gera um novo nome para o arquivo baseado no padrão.
        
        Formato: MM - MA 19a DDMMAAAA(XX) [- evento].extensão
        """
        data = info.data_preferencial
        mes_bebe = BabyAge.calculate_month(data)
        
        novo_nome = (
            f"{mes_bebe:02d} - MA 19a "
            f"{data.strftime('%d%m%Y')}"
            f"({numero_sequencial:02d})"
        )
        
        if eventos:
            data_fmt = data.strftime('%d%m%Y')
            if data_fmt in eventos:
                novo_nome = f"{novo_nome} - {eventos[data_fmt]}"
        
        return novo_nome + info.extensao
    
    def is_organized(self, nome_arquivo: str) -> bool:
        """
        Verifica se o arquivo já segue o padrão de organização.
        Formato: MM - MA 19a DDMMAAAA(XX)[- evento].extensão
        """
        nome_sem_ext = Path(nome_arquivo).stem
        padrao = r'^\d{2} - MA 19a \d{8}\(\d{2}\)(?:\s-\s.+)?$'
        return bool(re.match(padrao, nome_sem_ext))


class FileRenamer:
    """Responsável por renomear arquivos."""
    
    def __init__(self):
        self.filename_generator = FilenameGenerator()
    
    def rename_images(
        self,
        imagens: List[ImageInfo],
        diretorio: str,
        eventos: Optional[Dict[str, str]] = None,
        simular: bool = True
    ) -> int:
        """
        Renomeia as imagens de acordo com o formato especificado.
        
        Returns:
            Número de arquivos renomeados
        """
        if simular:
            print("\n🔄 SIMULAÇÃO: Renomeando arquivos...")
        else:
            print("\n✨ RENOMEANDO ARQUIVOS...")
        
        print("─" * 60)
        
        grupos = self._group_by_date(imagens)
        total_renomeados = 0
        total_erros = 0
        
        for _, imgs_do_dia in grupos.items():
            imgs_do_dia.sort(key=lambda x: x.data_preferencial)
            
            for idx, img in enumerate(imgs_do_dia):
                caminho_atual = os.path.join(diretorio, img.arquivo)
                novo_nome = self.filename_generator.generate_filename(
                    img, numero_sequencial=idx, eventos=eventos
                )
                novo_caminho = os.path.join(diretorio, novo_nome)
                
                if simular:
                    print(f"📄 {img.arquivo}")
                    print(f"   ➡️  {novo_nome}")
                else:
                    print(f"📄 Renomeando: {img.arquivo}")
                    try:
                        shutil.move(caminho_atual, novo_caminho)
                        total_renomeados += 1
                        print(f"   ✅ Sucesso: {novo_nome}")
                    except (IOError, OSError) as e:
                        total_erros += 1
                        print(f"   ❌ Erro: {e}")
        
        if not simular:
            print("─" * 60)
            print("📊 RESULTADO:")
            print(f"   ✅ Renomeados com sucesso: {total_renomeados}")
            print(f"   ❌ Erros: {total_erros}")
            print("─" * 60)
        
        return total_renomeados
    
    def _group_by_date(self, imagens: List[ImageInfo]) -> Dict[str, List[ImageInfo]]:
        """Agrupa imagens por data."""
        grupos: Dict[str, List[ImageInfo]] = {}
        for img in imagens:
            data = img.data_preferencial.strftime('%d%m%Y')
            if data not in grupos:
                grupos[data] = []
            grupos[data].append(img)
        return grupos
