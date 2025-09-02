import os
import shutil
from typing import Dict, List, Optional
from collections import defaultdict
from pathlib import Path

from ..domain.image import ImageInfo
from ..domain.configuration import ProjectConfiguration

class FolderOrganizer:
    
    def organize_by_years(
        self,
        images: List[ImageInfo],
        directory: str,
        simular: bool = True
    ) -> Dict[int, List[ImageInfo]]:
        
        if not images:
            return {}
        
        imagens_por_ano = defaultdict(list)
        
        for img in images:
            date = img.preferred_date
            ano = date.year
            imagens_por_ano[ano].append(img)
        
        if not imagens_por_ano:
            print("📅 Nenhuma imagem com date válida para organização.")
            return {}
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Organizando por anos...")
        else:
            print("\n📅 ORGANIZANDO POR ANOS...")
        
        print("─" * 70)
        
        total_organizadas = 0
        
        for ano, imgs_do_ano in sorted(imagens_por_ano.items()):
            pasta_ano = os.path.join(directory, f"Ano {ano}")
            
            print(f"\n📂 Ano {ano}")
            print(f"   📊 {len(imgs_do_ano)} imagem(ns) encontrada(s)")
            
            if simular:
                print(f"   📁 Criaria pasta: Ano {ano}/")
                for img in imgs_do_ano:
                    print(f"   📤 Moveria: {img.file}")
            else:
                if not os.path.exists(pasta_ano):
                    os.makedirs(pasta_ano)
                    print(f"   ✅ Pasta criada: Ano {ano}/")
                
                for img in imgs_do_ano:
                    origem = os.path.join(directory, img.file)
                    destino = os.path.join(pasta_ano, img.file)
                    
                    try:
                        shutil.move(origem, destino)
                        total_organizadas += 1
                        print(f"   📤 Movida: {img.file}")
                    except (IOError, OSError) as e:
                        print(f"   ❌ Erro ao mover {img.file}: {e}")
        
        print("─" * 70)
        if not simular:
            print(f"📊 RESULTADO: {total_organizadas} images organizadas")
        else:
            total_previsao = sum(
                len(imgs) for imgs in imagens_por_ano.values()
            )
            print(f"📊 PREVISÃO: {total_previsao} images seriam organizadas")
        print("─" * 70)
        
        return dict(imagens_por_ano)
    
    def organize_by_events(
        self,
        directory: str,
        eventos_detectados: Dict[str, List[str]],
        simular: bool = True
    ) -> int:
        
        if not eventos_detectados:
            print("📁 Nenhum evento detectado nos nomes dos arquivos.")
            return 0
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Organizando por pastas de events...")
        else:
            print("\n📁 ORGANIZANDO POR PASTAS DE EVENTOS...")
        
        print("─" * 70)
        
        total_movidos = 0
        
        for evento, arquivos in eventos_detectados.items():
            pasta_evento = os.path.join(directory, evento)
            
            print(f"\n📂 Evento: {evento}")
            print(f"   📊 {len(arquivos)} file(s) encontrado(s)")
            
            if simular:
                print(f"   📁 Criaria pasta: {evento}/")
                for file in arquivos:
                    print(f"   📤 Moveria: {file}")
            else:
                if not os.path.exists(pasta_evento):
                    os.makedirs(pasta_evento)
                    print(f"   ✅ Pasta criada: {evento}/")
                
                for file in arquivos:
                    origem = os.path.join(directory, file)
                    destino = os.path.join(pasta_evento, file)
                    
                    try:
                        shutil.move(origem, destino)
                        total_movidos += 1
                        print(f"   📤 Movido: {file}")
                    except (IOError, OSError) as e:
                        print(f"   ❌ Erro ao mover {file}: {e}")
        
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
    
    def organize_by_custom_periods(
        self,
        images: List[ImageInfo],
        directory: str,
        configuration: ProjectConfiguration,
        simular: bool = True
    ) -> Dict[str, List[ImageInfo]]:
        
        if not images:
            return {}
        
        imagens_periodo_atual = []
        imagens_periodo_futuro = []
        nova_config = None
        
        for img in images:
            date = img.preferred_date
            
            if configuration.is_date_in_range(date):
                imagens_periodo_atual.append(img)
            elif configuration.should_create_new_period(date):
                imagens_periodo_futuro.append(img)
                if nova_config is None:
                    nova_config = configuration.suggest_new_period_config(date)
        
        result = {}
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Organizando por períodos customizados...")
        else:
            print("\n📅 ORGANIZANDO POR PERÍODOS CUSTOMIZADOS...")
        
        print("─" * 70)
        
        if imagens_periodo_atual:
            nome_pasta_atual = self._gerar_nome_pasta_periodo(configuration)
            result[nome_pasta_atual] = imagens_periodo_atual
            
            if not simular:
                self._criar_pasta_e_mover(
                    imagens_periodo_atual,
                    directory,
                    nome_pasta_atual
                )
            
            print(f"📁 {nome_pasta_atual}: {len(imagens_periodo_atual)} images")
        
        if imagens_periodo_futuro and nova_config:
            nome_pasta_futura = self._gerar_nome_pasta_periodo(nova_config)
            result[nome_pasta_futura] = imagens_periodo_futuro
            
            if not simular:
                self._criar_pasta_e_mover(
                    imagens_periodo_futuro,
                    directory,
                    nome_pasta_futura
                )
            
            print(f"📁 {nome_pasta_futura}: "
                  f"{len(imagens_periodo_futuro)} images")
            print("   ⚠️  Novo período detectado!")
        
        if not result:
            print("📅 Nenhuma imagem para organizar por períodos.")
        
        print("─" * 70)
        return result
    
    def _gerar_nome_pasta_periodo(self, config: ProjectConfiguration) -> str:
        
        inicio = config.start_date.strftime("%d-%m-%Y")
        if config.end_date:
            final = config.end_date.strftime("%d-%m-%Y")
        else:
            final = "indefinido"
        prefix = config.naming_prefix.replace(" ", "_")
        
        return f"{prefix}_{inicio}_a_{final}"
    
    def _criar_pasta_e_mover(
        self,
        images: List[ImageInfo],
        diretorio_base: str,
        folder_name: str
    ) -> None:
        
        caminho_pasta = os.path.join(diretorio_base, folder_name)
        
        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)
            print(f"   ✅ Pasta criada: {folder_name}")
        
        for img in images:
            origem = img.file
            filename = os.path.basename(origem)
            destino = os.path.join(caminho_pasta, filename)
            
            try:
                shutil.move(origem, destino)
                
                img.file = destino
            except Exception as e:
                print(f"   ❌ Erro ao mover {filename}: {e}")

    def detect_events_in_files(self, images: List[ImageInfo]) -> Dict[str, List[str]]:
        
        eventos_detectados = defaultdict(list)
        
        for img in images:
            if self._is_organized(img.file):
                nome_sem_ext = Path(img.file).stem
                if ' - ' in nome_sem_ext:
                    partes = nome_sem_ext.split(' - ')
                    if len(partes) >= 3:
                        evento = ' - '.join(partes[2:])
                        eventos_detectados[evento].append(img.file)
        
        return dict(eventos_detectados)
    
    def _is_organized(self, filename: str) -> bool:
        
        from .file_renamer import FilenameGenerator
        generator = FilenameGenerator()
        return generator.is_organized(filename)