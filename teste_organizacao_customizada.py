#!/usr/bin/env python3
"""
Teste da funcionalidade de organização por períodos customizados
"""

from datetime import datetime
from src.domain.configuration import ProjectConfiguration
from src.services.folder_organizer import FolderOrganizer
from src.domain.image import ImageInfo, PeriodCalculator


def teste_organizacao_customizada():
    """Testa a organização por períodos customizados"""
    print("🧪 TESTANDO ORGANIZAÇÃO POR PERÍODOS CUSTOMIZADOS")
    print("=" * 60)
    
    # Criar configuração de teste
    data_inicio = datetime(2024, 1, 15)
    data_final = datetime(2025, 1, 15)  # +1 ano automático
    
    config = ProjectConfiguration(
        data_inicio=data_inicio,
        data_final=data_final,
        prefixo_nomenclatura="projeto",
        incluir_periodo=True,
        incluir_sequencial=True
    )
    
    print("📅 Configuração:")
    print(f"   Data início: {config.data_inicio.strftime('%d/%m/%Y')}")
    if config.data_final:
        print(f"   Data final: {config.data_final.strftime('%d/%m/%Y')}")
    print(f"   Prefixo: {config.prefixo_nomenclatura}")
    print(f"   Período: {'Sim' if config.incluir_periodo else 'Não'}")
    print(f"   Sequencial: {'Sim' if config.incluir_sequencial else 'Não'}")
    
    # Criar images de teste para diferentes períodos
    calculator = PeriodCalculator(config.data_inicio)
    
    # Imagem no período 00 (15/01 a 14/02)
    img1 = ImageInfo(
        arquivo="img1.jpg",
        formato="JPEG",
        dimensoes=(1920, 1080),
        modo="RGB",
        tamanho=1024000,
        data_mod=datetime(2024, 1, 20)
    )
    periodo1 = calculator.calculate_month(img1.data_preferencial)
    print(f"\n📷 Imagem 1 (20/01/2024): Período {periodo1:02d}")
    
    # Imagem no período 01 (15/02 a 14/03)
    img2 = ImageInfo(
        arquivo="img2.jpg",
        formato="JPEG",
        dimensoes=(1920, 1080),
        modo="RGB",
        tamanho=1024000,
        data_mod=datetime(2024, 2, 20)
    )
    periodo2 = calculator.calculate_month(img2.data_preferencial)
    print(f"📷 Imagem 2 (20/02/2024): Período {periodo2:02d}")
    
    # Imagem no período 12 (15/01/2025 - fora do período configurado)
    img3 = ImageInfo(
        arquivo="img3.jpg",
        formato="JPEG",
        dimensoes=(1920, 1080),
        modo="RGB",
        tamanho=1024000,
        data_mod=datetime(2025, 1, 20)
    )
    periodo3 = calculator.calculate_month(img3.data_preferencial)
    print(f"📷 Imagem 3 (20/01/2025): Período {periodo3:02d} "
          f"⚠️  FORA DO PERÍODO")
    
    # Teste do organizador
    organizer = FolderOrganizer()
    imagens = [img1, img2, img3]
    
    print("\n🔍 Testando organização...")
    resultado = organizer.organize_by_custom_periods(
        imagens, "/tmp/teste", config, simular=True
    )
    
    print("\n📊 Resultado:")
    for pasta, imgs in resultado.items():
        print(f"   📁 {pasta}: {len(imgs)} imagens")
        for img in imgs:
            periodo = calculator.calculate_month(img.data_preferencial)
            print(f"      - {img.arquivo} (período {periodo:02d})")
    
    print("\n✅ Teste concluído!")


if __name__ == "__main__":
    teste_organizacao_customizada()
