import re
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

from ..domain.image import ImageInfo, Event
from ..domain.configuration import ProjectConfiguration, ConfigurationManager

class FilenameGenerator:
    
    def __init__(self, configuration: Optional[ProjectConfiguration] = None):
        
        if configuration is None:
            from datetime import datetime
            configuration = ConfigurationManager.create_custom_configuration(
                data_inicio=datetime.now().replace(month=1, day=1),
                prefixo="IMG",
                incluir_periodo=True
            )
        self.configuration = configuration
    
    def generate_filename(
        self,
        info: ImageInfo,
        numero_sequencial: int = 0,
        eventos: Optional[Dict[str, str]] = None
    ) -> str:
        
        data = info.data_preferencial
        
        if not self.configuration.is_date_in_range(data):
            
            nome_base = data.strftime(self.configuration.formato_data)
            if self.configuration.incluir_sequencial:
                nome_base += f"({numero_sequencial:02d})"
        else:
            
            evento_str = None
            if eventos:
                data_fmt = data.strftime('%d%m%Y')
                evento_str = eventos.get(data_fmt)
            
            nome_base = self.configuration.generate_filename_pattern(
                data, numero_sequencial, evento_str
            )
        
        return nome_base + info.extensao
    
    def is_organized(self, nome_arquivo: str) -> bool:
        
        nome_sem_ext = Path(nome_arquivo).stem
        
        padrao_antigo = r'^\d{2} - IMG \d{8}\(\d{2}\)(?:\s-\s.+)?$'
        
        padrao_novo = r'.*\d{8}\(\d{2}\)(?:\s-\s.+)?$'
        
        return (
            bool(re.match(padrao_antigo, nome_sem_ext)) or
            bool(re.match(padrao_novo, nome_sem_ext))
        )

class FileRenamer:
    
    def __init__(self):
        self.filename_generator = FilenameGenerator()
    
    def rename_images(
        self,
        imagens: List[ImageInfo],
        diretorio: str,
        eventos: Optional[Dict[str, str]] = None,
        simular: bool = True
    ) -> int:
        
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
        
        grupos: Dict[str, List[ImageInfo]] = {}
        for img in imagens:
            data = img.data_preferencial.strftime('%d%m%Y')
            if data not in grupos:
                grupos[data] = []
            grupos[data].append(img)
        return grupos