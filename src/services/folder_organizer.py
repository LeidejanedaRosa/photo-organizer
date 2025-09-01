import os
import shutil
from typing import Dict, List, Optional
from collections import defaultdict
from pathlib import Path

from ..domain.image import ImageInfo
from ..domain.configuration import ProjectConfiguration


class FolderOrganizer:
    """Responsável por organizar imagens em pastas."""
    
    def organize_by_years(
        self,
        imagens: List[ImageInfo],
        diretorio: str,
        simular: bool = True
    ) -> Dict[int, List[ImageInfo]]:
        """
        Organiza imagens automaticamente por ano.
        
        Returns:
            Dicionário com ano -> lista de imagens
        """
        if not imagens:
            return {}
        
        imagens_por_ano = defaultdict(list)
        
        for img in imagens:
            data = img.data_preferencial
            ano = data.year
            imagens_por_ano[ano].append(img)
        
        if not imagens_por_ano:
            print("📅 Nenhuma imagem com data válida para organização.")
            return {}
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Organizando por anos...")
        else:
            print("\n📅 ORGANIZANDO POR ANOS...")
        
        print("─" * 70)
        
        total_organizadas = 0
        
        for ano, imgs_do_ano in sorted(imagens_por_ano.items()):
            pasta_ano = os.path.join(diretorio, f"Ano {ano}")
            
            print(f"\n📂 Ano {ano}")
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
    
    def organize_by_custom_periods(
        self,
        imagens: List[ImageInfo],
        diretorio: str,
        configuration: ProjectConfiguration,
        simular: bool = True
    ) -> Dict[str, List[ImageInfo]]:
        """
        Organiza imagens por períodos customizados.
        Cria pastas para períodos atual e futuros conforme necessário.
        
        Returns:
            Dicionário com pasta -> lista de imagens
        """
        if not imagens:
            return {}
        
        # Separa imagens por período
        imagens_periodo_atual = []
        imagens_periodo_futuro = []
        nova_config = None
        
        for img in imagens:
            data = img.data_preferencial
            
            if configuration.is_date_in_range(data):
                imagens_periodo_atual.append(img)
            elif configuration.should_create_new_period(data):
                imagens_periodo_futuro.append(img)
                if nova_config is None:
                    nova_config = configuration.suggest_new_period_config(data)
        
        resultado = {}
        
        if simular:
            print("\n🔄 SIMULAÇÃO: Organizando por períodos customizados...")
        else:
            print("\n📅 ORGANIZANDO POR PERÍODOS CUSTOMIZADOS...")
        
        print("─" * 70)
        
        # Organiza período atual
        if imagens_periodo_atual:
            nome_pasta_atual = self._gerar_nome_pasta_periodo(configuration)
            resultado[nome_pasta_atual] = imagens_periodo_atual
            
            if not simular:
                self._criar_pasta_e_mover(
                    imagens_periodo_atual,
                    diretorio,
                    nome_pasta_atual
                )
            
            print(f"📁 {nome_pasta_atual}: {len(imagens_periodo_atual)} imagens")
        
        # Organiza período futuro (se houver)
        if imagens_periodo_futuro and nova_config:
            nome_pasta_futura = self._gerar_nome_pasta_periodo(nova_config)
            resultado[nome_pasta_futura] = imagens_periodo_futuro
            
            if not simular:
                self._criar_pasta_e_mover(
                    imagens_periodo_futuro,
                    diretorio,
                    nome_pasta_futura
                )
            
            print(f"📁 {nome_pasta_futura}: "
                  f"{len(imagens_periodo_futuro)} imagens")
            print("   ⚠️  Novo período detectado!")
        
        if not resultado:
            print("📅 Nenhuma imagem para organizar por períodos.")
        
        print("─" * 70)
        return resultado
    
    def _gerar_nome_pasta_periodo(self, config: ProjectConfiguration) -> str:
        """Gera nome da pasta baseado na configuração do período."""
        inicio = config.data_inicio.strftime("%d-%m-%Y")
        if config.data_final:
            final = config.data_final.strftime("%d-%m-%Y")
        else:
            final = "indefinido"
        prefixo = config.prefixo_nomenclatura.replace(" ", "_")
        
        return f"{prefixo}_{inicio}_a_{final}"
    
    def _criar_pasta_e_mover(
        self,
        imagens: List[ImageInfo],
        diretorio_base: str,
        nome_pasta: str
    ) -> None:
        """Cria pasta e move imagens para ela."""
        caminho_pasta = os.path.join(diretorio_base, nome_pasta)
        
        # Cria pasta se não existir
        if not os.path.exists(caminho_pasta):
            os.makedirs(caminho_pasta)
            print(f"   ✅ Pasta criada: {nome_pasta}")
        
        # Move imagens
        for img in imagens:
            origem = img.arquivo
            nome_arquivo = os.path.basename(origem)
            destino = os.path.join(caminho_pasta, nome_arquivo)
            
            try:
                shutil.move(origem, destino)
                # Atualiza o caminho da imagem
                img.arquivo = destino
            except Exception as e:
                print(f"   ❌ Erro ao mover {nome_arquivo}: {e}")

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
