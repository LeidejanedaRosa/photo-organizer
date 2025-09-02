from datetime import datetime
from typing import List
from collections import defaultdict

from ..domain.image import ImageInfo

class ReportGenerator:
    
    def generate_detailed_report(self, images: List[ImageInfo]) -> None:
        
        if not images:
            print("📋 Nenhuma imagem para analisar no relatório.")
            return
        
        print("\n" + "=" * 70)
        print("📊 RELATÓRIO DETALHADO DAS IMAGENS")
        print("=" * 70)
        
        total_imagens = len(images)
        total_tamanho = sum(img.tamanho for img in images)
        
        self._analyze_formats(images, total_imagens)
        self._analyze_dimensions(images, total_imagens)
        self._analyze_temporal_data(images, total_imagens, total_tamanho)
        
        print("=" * 70)
    
    def _analyze_formats(self, images: List[ImageInfo], total: int) -> None:
        
        formatos = defaultdict(int)
        tamanhos_por_formato = defaultdict(int)
        
        for img in images:
            formatos[img.formato] += 1
            tamanhos_por_formato[img.formato] += img.tamanho
        
        print("\n🎨 DISTRIBUIÇÃO POR FORMATO:")
        for formato, count in sorted(formatos.items()):
            tamanho_mb = tamanhos_por_formato[formato] / (1024*1024)
            porcentagem = (count / total) * 100
            print(
                f"   📄 {formato}: {count} arquivos ({porcentagem:.1f}%) - "
                f"{tamanho_mb:.2f} MB"
            )
    
    def _analyze_dimensions(self, images: List[ImageInfo], total: int) -> None:
        
        dimensions = defaultdict(int)
        
        for img in images:
            dim_str = f"{img.dimensions[0]}x{img.dimensions[1]}"
            dimensions[dim_str] += 1
        
        print("\n📐 RESOLUÇÕES MAIS COMUNS:")
        top_dimensoes = sorted(
            dimensions.items(), key=lambda x: x[1], reverse=True
        )[:5]
        for dim, count in top_dimensoes:
            porcentagem = (count / total) * 100
            print(f"   🖼️  {dim}: {count} images ({porcentagem:.1f}%)")
    
    def _analyze_temporal_data(
        self, 
        images: List[ImageInfo], 
        total: int, 
        total_tamanho: int
    ) -> None:
        
        print("\n📈 ESTATÍSTICAS GERAIS:")
        print(f"   📷 Total de images: {total}")
        print(f"   💾 Tamanho total: {total_tamanho / (1024*1024):.2f} MB")
        print(f"   📏 Tamanho médio: {total_tamanho / total / 1024:.1f} KB")
        
        if images:
            datas = [img.preferred_date for img in images]
            data_mais_antiga = min(datas)
            data_mais_recente = max(datas)
            period = (data_mais_recente - data_mais_antiga).days
            
            print("\n⏰ ANÁLISE TEMPORAL:")
            print(
                f"   📆 Foto mais antiga: "
                f"{data_mais_antiga.strftime('%d/%m/%Y %H:%M')}"
            )
            print(
                f"   📆 Foto mais recente: "
                f"{data_mais_recente.strftime('%d/%m/%Y %H:%M')}"
            )
            print(f"   📊 Período abrangido: {period} dias")
            
            if period > 0:
                frequencia = total / period
                print(f"   📈 Frequência média: {frequencia:.2f} fotos/dia")
    
    def search_photos_by_period(
        self,
        images: List[ImageInfo],
        start_date: str,
        end_date: str
    ) -> List[ImageInfo]:
        
        try:
            inicio = datetime.strptime(start_date, '%d/%m/%Y')
            fim = datetime.strptime(end_date, '%d/%m/%Y')
            fim = fim.replace(hour=23, minute=59, second=59)
            
            period_photos = []
            for img in images:
                data_foto = img.preferred_date
                if inicio <= data_foto <= fim:
                    period_photos.append(img)
            
            return period_photos
        except ValueError:
            print("❌ Formato de date inválido! Use DD/MM/AAAA")
            return []