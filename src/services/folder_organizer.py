import os
import shutil
from typing import Dict, List
from collections import defaultdict
from pathlib import Path

from ..domain.image import ImageInfo, BabyAge


class FolderOrganizer:
    """Responsável por organizar imagens em pastas."""
    
    def organize_by_years(
        self,
        imagens: List[ImageInfo],
        diretorio: str,
        simular: bool = True
    ) -> Dict[int, List[ImageInfo]]:
        """
        Organiza imagens automaticamente por ano do bebê.
        
        Returns:
            Dicionário com ano -> lista de imagens
        """
        if not imagens:
            return {}
        
        imagens_por_ano = defaultdict(list)
        
        for img in imagens:
            data = img.data_preferencial
            ano_bebe = BabyAge.calculate_year(data)
            if ano_bebe > 0:
                imagens_por_ano[ano_bebe].append(img)
        
        if not imagens_por_ano:
            print("📅 Nenhuma imagem com data válida para organização.")
            return {}
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Organizando por anos do bebê...")
        else:
            print("\n📅 ORGANIZANDO POR ANOS DO BEBÊ...")
        
        print("─" * 70)
        
        total_organizadas = 0
        
        for ano, imgs_do_ano in sorted(imagens_por_ano.items()):
            pasta_ano = os.path.join(diretorio, f"Ano {ano}")
            
            print(f"\n📂 Ano {ano} do bebê")
            print(f"   📊 {len(imgs_do_ano)} imagem(ns) encontrada(s)")
            
            if simular:
                print(f"   📁 Criaria pasta: Ano {ano}/")
                for img in imgs_do_ano:
                    print(f"   📤 Moveria: {img.arquivo}")
            else:
                if not os.path.exists(pasta_ano):
                    os.makedirs(pasta_ano)
                    print(f"   ✅ Pasta criada: Ano {ano}/")
                
                for img in imgs_do_ano:
                    origem = os.path.join(diretorio, img.arquivo)
                    destino = os.path.join(pasta_ano, img.arquivo)
                    
                    try:
                        shutil.move(origem, destino)
                        total_organizadas += 1
                        print(f"   📤 Movida: {img.arquivo}")
                    except (IOError, OSError) as e:
                        print(f"   ❌ Erro ao mover {img.arquivo}: {e}")
        
        print("─" * 70)
        if not simular:
            print(f"📊 RESULTADO: {total_organizadas} imagens organizadas")
        else:
            total_previsao = sum(
                len(imgs) for imgs in imagens_por_ano.values()
            )
            print(f"📊 PREVISÃO: {total_previsao} imagens seriam organizadas")
        print("─" * 70)
        
        return dict(imagens_por_ano)
    
    def organize_by_events(
        self,
        diretorio: str,
        eventos_detectados: Dict[str, List[str]],
        simular: bool = True
    ) -> int:
        """
        Organiza as fotos em pastas baseadas nos eventos detectados.
        
        Returns:
            Número de arquivos movidos
        """
        if not eventos_detectados:
            print("📁 Nenhum evento detectado nos nomes dos arquivos.")
            return 0
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Organizando por pastas de eventos...")
        else:
            print("\n📁 ORGANIZANDO POR PASTAS DE EVENTOS...")
        
        print("─" * 70)
        
        total_movidos = 0
        
        for evento, arquivos in eventos_detectados.items():
            pasta_evento = os.path.join(diretorio, evento)
            
            print(f"\n📂 Evento: {evento}")
            print(f"   📊 {len(arquivos)} arquivo(s) encontrado(s)")
            
            if simular:
                print(f"   📁 Criaria pasta: {evento}/")
                for arquivo in arquivos:
                    print(f"   📤 Moveria: {arquivo}")
            else:
                if not os.path.exists(pasta_evento):
                    os.makedirs(pasta_evento)
                    print(f"   ✅ Pasta criada: {evento}/")
                
                for arquivo in arquivos:
                    origem = os.path.join(diretorio, arquivo)
                    destino = os.path.join(pasta_evento, arquivo)
                    
                    try:
                        shutil.move(origem, destino)
                        total_movidos += 1
                        print(f"   📤 Movido: {arquivo}")
                    except (IOError, OSError) as e:
                        print(f"   ❌ Erro ao mover {arquivo}: {e}")
        
        print("─" * 70)
        if not simular:
            print(f"📊 RESULTADO: {total_movidos} arquivos organizados")
        else:
            total_previsao = sum(
                len(arquivos) for arquivos in eventos_detectados.values()
            )
            print(f"📊 PREVISÃO: {total_previsao} arquivos organizados")
        print("─" * 70)
        
        return total_movidos
    
    def detect_events_in_files(self, imagens: List[ImageInfo]) -> Dict[str, List[str]]:
        """
        Detecta eventos nos nomes dos arquivos já organizados.
        
        Returns:
            Dicionário com evento -> lista de arquivos
        """
        eventos_detectados = defaultdict(list)
        
        for img in imagens:
            if self._is_organized(img.arquivo):
                nome_sem_ext = Path(img.arquivo).stem
                if ' - ' in nome_sem_ext:
                    partes = nome_sem_ext.split(' - ')
                    if len(partes) >= 3:
                        evento = ' - '.join(partes[2:])
                        eventos_detectados[evento].append(img.arquivo)
        
        return dict(eventos_detectados)
    
    def _is_organized(self, nome_arquivo: str) -> bool:
        """Verifica se o arquivo já está organizado."""
        from .file_renamer import FilenameGenerator
        generator = FilenameGenerator()
        return generator.is_organized(nome_arquivo)
