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
                start_date=datetime.now().replace(month=1, day=1),
                prefix="IMG",
                include_period=True
            )
        self.configuration = configuration
    
    def generate_filename(
        self,
        info: ImageInfo,
        numero_sequencial: int = 0,
        events: Optional[Dict[str, str]] = None
    ) -> str:
        
        date = info.preferred_date
        
        if not self.configuration.is_date_in_range(date):
            
            nome_base = date.strftime(self.configuration.date_format)
            if self.configuration.include_sequential:
                nome_base += f"({numero_sequencial:02d})"
        else:
            
            evento_str = None
            if events:
                date_fmt = date.strftime('%d%m%Y')
                evento_str = events.get(date_fmt)
            
            nome_base = self.configuration.generate_filename_pattern(
                date, numero_sequencial, evento_str
            )
        
        return nome_base + info.extension
    
    def is_organized(self, filename: str) -> bool:
        
        nome_sem_ext = Path(filename).stem
        
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
        images: List[ImageInfo],
        directory: str,
        events: Optional[Dict[str, str]] = None,
        simular: bool = True
    ) -> int:
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Renomeando arquivos...")
        else:
            print("\n✨ RENOMEANDO ARQUIVOS...")
        
        print("─" * 60)
        
        grupos = self._group_by_date(images)
        total_renomeados = 0
        total_erros = 0
        
        for _, imgs_do_dia in grupos.items():
            imgs_do_dia.sort(key=lambda x: x.preferred_date)
            
            for idx, img in enumerate(imgs_do_dia):
                caminho_atual = os.path.join(directory, img.file)
                novo_nome = self.filename_generator.generate_filename(
                    img, numero_sequencial=idx, events=events
                )
                novo_caminho = os.path.join(directory, novo_nome)
                
                if simular:
                    print(f"📄 {img.file}")
                    print(f"   ➡️  {novo_nome}")
                else:
                    print(f"📄 Renomeando: {img.file}")
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
    
    def _group_by_date(self, images: List[ImageInfo]) -> Dict[str, List[ImageInfo]]:
        
        grupos: Dict[str, List[ImageInfo]] = {}
        for img in images:
            date = img.preferred_date.strftime('%d%m%Y')
            if date not in grupos:
                grupos[date] = []
            grupos[date].append(img)
        return grupos