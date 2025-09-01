from typing import Dict, List, Optional

from ..domain.image import ImageInfo
from .image_analyzer import ImageAnalyzer
from .duplicate_manager import DuplicateManager
from .file_renamer import FileRenamer, FilenameGenerator
from .folder_organizer import FolderOrganizer
from .backup_manager import BackupManager
from .report_generator import ReportGenerator


class PhotoOrganizerService:
    """
    Serviço principal que orquestra todas as operações de organização de fotos.
    Segue o princípio Single Responsibility - cada serviço tem uma responsabilidade.
    """
    
    def __init__(self):
        self.image_analyzer = ImageAnalyzer()
        self.duplicate_manager = DuplicateManager()
        self.file_renamer = FileRenamer()
        self.folder_organizer = FolderOrganizer()
        self.backup_manager = BackupManager()
        self.report_generator = ReportGenerator()
        self.filename_generator = FilenameGenerator()
    
    def analyze_directory(self, diretorio: str) -> tuple[List[ImageInfo], List[ImageInfo]]:
        """
        Analisa um diretório e separa imagens organizadas das não organizadas.
        
        Returns:
            Tupla (imagens_não_organizadas, imagens_organizadas)
        """
        todas_imagens = self.image_analyzer.analyze_directory(diretorio)
        
        imagens_organizadas = []
        imagens_nao_organizadas = []
        
        for img in todas_imagens:
            if self.filename_generator.is_organized(img.arquivo):
                imagens_organizadas.append(img)
            else:
                imagens_nao_organizadas.append(img)
        
        # Ordena por data
        key_func = lambda x: x.data_preferencial
        imagens_organizadas.sort(key=key_func)
        imagens_nao_organizadas.sort(key=key_func)
        
        return imagens_nao_organizadas, imagens_organizadas
    
    def detect_and_move_duplicates(
        self, 
        imagens: List[ImageInfo], 
        diretorio: str, 
        simular: bool = True
    ) -> int:
        """Detecta e move duplicatas."""
        duplicadas = self.duplicate_manager.find_duplicates(imagens)
        if duplicadas and not simular:
            backup_file = self.backup_manager.create_backup(diretorio, "mover_duplicatas")
            print(f"💾 Backup criado: {backup_file}")
        
        return self.duplicate_manager.move_duplicates(duplicadas, diretorio, simular)
    
    def rename_images(
        self, 
        imagens: List[ImageInfo], 
        diretorio: str, 
        eventos: Optional[Dict[str, str]] = None,
        simular: bool = True
    ) -> int:
        """Renomeia imagens seguindo o padrão estabelecido."""
        if not simular and imagens:
            backup_file = self.backup_manager.create_backup(diretorio, "renomear_imagens")
            print(f"💾 Backup criado: {backup_file}")
        
        return self.file_renamer.rename_images(imagens, diretorio, eventos, simular)
    
    def organize_by_years(
        self, 
        imagens: List[ImageInfo], 
        diretorio: str, 
        simular: bool = True
    ) -> Dict[int, List[ImageInfo]]:
        """Organiza imagens por anos do bebê."""
        if not simular and imagens:
            backup_file = self.backup_manager.create_backup(diretorio, "organizar_anos")
            print(f"💾 Backup criado: {backup_file}")
        
        return self.folder_organizer.organize_by_years(imagens, diretorio, simular)
    
    def organize_by_events(
        self, 
        imagens: List[ImageInfo], 
        diretorio: str, 
        simular: bool = True
    ) -> int:
        """Organiza imagens por eventos detectados."""
        eventos_detectados = self.folder_organizer.detect_events_in_files(imagens)
        
        if not simular and eventos_detectados:
            backup_file = self.backup_manager.create_backup(diretorio, "organizar_eventos")
            print(f"💾 Backup criado: {backup_file}")
        
        return self.folder_organizer.organize_by_events(diretorio, eventos_detectados, simular)
    
    def generate_report(self, imagens: List[ImageInfo]) -> None:
        """Gera relatório detalhado das imagens."""
        self.report_generator.generate_detailed_report(imagens)
    
    def search_photos_by_period(
        self, 
        imagens: List[ImageInfo], 
        data_inicio: str, 
        data_fim: str
    ) -> List[ImageInfo]:
        """Busca fotos por período."""
        return self.report_generator.search_photos_by_period(imagens, data_inicio, data_fim)
    
    def create_manual_backup(self, diretorio: str) -> str:
        """Cria backup manual."""
        return self.backup_manager.create_backup(diretorio, "backup_manual")
    
    def print_analysis_statistics(
        self, 
        imagens_nao_organizadas: List[ImageInfo], 
        imagens_organizadas: List[ImageInfo]
    ) -> None:
        """Imprime estatísticas da análise."""
        total_imagens = len(imagens_nao_organizadas) + len(imagens_organizadas)
        
        print("\n📊 ESTATÍSTICAS:")
        print(f"Total de imagens encontradas: {total_imagens}")
        print(f"Já organizadas: {len(imagens_organizadas)}")
        print(f"Precisam ser organizadas: {len(imagens_nao_organizadas)}")
        
        if imagens_organizadas:
            print(f"\n✅ IMAGENS JÁ ORGANIZADAS ({len(imagens_organizadas)}):")
            for img in imagens_organizadas:
                print(f"  - {img.arquivo}")
        
        if not imagens_nao_organizadas:
            print("\n🎉 Todas as imagens já estão organizadas!")
            return
        
        print(f"\n📋 IMAGENS PARA ORGANIZAR ({len(imagens_nao_organizadas)}):")
        self._print_image_details(imagens_nao_organizadas)
    
    def _print_image_details(self, imagens: List[ImageInfo]) -> None:
        """Imprime detalhes das imagens."""
        from ..domain.image import BabyAge
        
        for img in imagens:
            data = img.data_preferencial
            mes_bebe = BabyAge.calculate_month(data)
            
            print(f"Arquivo: {img.arquivo}")
            print(f"Formato: {img.formato}")
            print(f"Dimensões: {img.dimensoes}")
            print(f"Modo: {img.modo}")
            print(f"Tamanho (bytes): {img.tamanho}")
            print(f"Data de modificação: {img.data_mod.strftime('%d/%m/%Y %H:%M:%S')}")
            if img.data_exif:
                print(f"Data EXIF: {img.data_exif.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"Mês do bebê: {mes_bebe:02d}")
            print("-" * 40)
