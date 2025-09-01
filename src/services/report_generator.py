from datetime import datetime
from typing import List
from collections import defaultdict

from ..domain.image import ImageInfo, BabyAge


class ReportGenerator:
    """Responsável por gerar relatórios detalhados das imagens."""
    
    def generate_detailed_report(self, imagens: List[ImageInfo]) -> None:
        """Gera um relatório detalhado das imagens analisadas."""
        if not imagens:
            print("📋 Nenhuma imagem para analisar no relatório.")
            return
        
        print("\n" + "=" * 70)
        print("📊 RELATÓRIO DETALHADO DAS IMAGENS")
        print("=" * 70)
        
        # Estatísticas gerais
        total_imagens = len(imagens)
        total_tamanho = sum(img.tamanho for img in imagens)
        
        # Análises específicas
        self._analyze_formats(imagens, total_imagens)
        self._analyze_baby_months(imagens, total_imagens)
        self._analyze_dimensions(imagens, total_imagens)
        self._analyze_temporal_data(imagens, total_imagens, total_tamanho)
        
        print("=" * 70)
    
    def _analyze_formats(self, imagens: List[ImageInfo], total: int) -> None:
        """Analisa distribuição por formato."""
        formatos = defaultdict(int)
        tamanhos_por_formato = defaultdict(int)
        
        for img in imagens:
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
    
    def _analyze_baby_months(self, imagens: List[ImageInfo], total: int) -> None:
        """Analisa distribuição por mês do bebê."""
        meses_bebe = defaultdict(int)
        
        for img in imagens:
            data = img.data_preferencial
            mes = BabyAge.calculate_month(data)
            meses_bebe[mes] += 1
        
        print("\n📅 DISTRIBUIÇÃO POR MÊS DO BEBÊ:")
        for mes in sorted(meses_bebe.keys()):
            count = meses_bebe[mes]
            porcentagem = (count / total) * 100
            print(f"   🗓️  Mês {mes:02d}: {count} fotos ({porcentagem:.1f}%)")
    
    def _analyze_dimensions(self, imagens: List[ImageInfo], total: int) -> None:
        """Analisa distribuição por dimensões."""
        dimensoes = defaultdict(int)
        
        for img in imagens:
            dim_str = f"{img.dimensoes[0]}x{img.dimensoes[1]}"
            dimensoes[dim_str] += 1
        
        print("\n📐 RESOLUÇÕES MAIS COMUNS:")
        top_dimensoes = sorted(
            dimensoes.items(), key=lambda x: x[1], reverse=True
        )[:5]
        for dim, count in top_dimensoes:
            porcentagem = (count / total) * 100
            print(f"   🖼️  {dim}: {count} imagens ({porcentagem:.1f}%)")
    
    def _analyze_temporal_data(
        self, 
        imagens: List[ImageInfo], 
        total: int, 
        total_tamanho: int
    ) -> None:
        """Analisa dados temporais das imagens."""
        print("\n📈 ESTATÍSTICAS GERAIS:")
        print(f"   📷 Total de imagens: {total}")
        print(f"   💾 Tamanho total: {total_tamanho / (1024*1024):.2f} MB")
        print(f"   📏 Tamanho médio: {total_tamanho / total / 1024:.1f} KB")
        
        if imagens:
            datas = [img.data_preferencial for img in imagens]
            data_mais_antiga = min(datas)
            data_mais_recente = max(datas)
            periodo = (data_mais_recente - data_mais_antiga).days
            
            print("\n⏰ ANÁLISE TEMPORAL:")
            print(
                f"   📆 Foto mais antiga: "
                f"{data_mais_antiga.strftime('%d/%m/%Y %H:%M')}"
            )
            print(
                f"   📆 Foto mais recente: "
                f"{data_mais_recente.strftime('%d/%m/%Y %H:%M')}"
            )
            print(f"   📊 Período abrangido: {periodo} dias")
            
            if periodo > 0:
                frequencia = total / periodo
                print(f"   📈 Frequência média: {frequencia:.2f} fotos/dia")
    
    def search_photos_by_period(
        self,
        imagens: List[ImageInfo],
        data_inicio: str,
        data_fim: str
    ) -> List[ImageInfo]:
        """
        Busca fotos em um período específico.
        Formato das datas: DD/MM/AAAA
        """
        try:
            inicio = datetime.strptime(data_inicio, '%d/%m/%Y')
            fim = datetime.strptime(data_fim, '%d/%m/%Y')
            fim = fim.replace(hour=23, minute=59, second=59)
            
            fotos_periodo = []
            for img in imagens:
                data_foto = img.data_preferencial
                if inicio <= data_foto <= fim:
                    fotos_periodo.append(img)
            
            return fotos_periodo
        except ValueError:
            print("❌ Formato de data inválido! Use DD/MM/AAAA")
            return []
