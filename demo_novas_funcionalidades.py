#!/usr/bin/env python3
"""
Demonstração das novas funcionalidades do Organizador de Fotos v2.0
"""
from datetime import datetime
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.domain.configuration import ConfigurationManager
from src.services.file_renamer import FilenameGenerator
from src.domain.image import ImageInfo


def demo_configuracoes():
    """Demonstra diferentes tipos de configuração."""
    print("🎯 DEMONSTRAÇÃO - CONFIGURAÇÕES PERSONALIZADAS")
    print("=" * 60)
    
    # 1. Configuração para projeto de viagem
    print("1️⃣  PROJETO VIAGEM 2023")
    print("-" * 30)
    config_viagem = ConfigurationManager.create_custom_configuration(
        data_inicio=datetime(2023, 6, 1),
        data_final=datetime(2023, 8, 31),
        prefixo="VIAGEM",
        incluir_periodo=True
    )
    
    datas_viagem = [
        datetime(2023, 6, 15),  # Início da viagem
        datetime(2023, 7, 20),  # Meio da viagem
        datetime(2023, 8, 10),  # Final da viagem
    ]
    
    generator_viagem = FilenameGenerator(config_viagem)
    
    for i, data in enumerate(datas_viagem):
        # Simula uma imagem
        img = type('MockImage', (), {
            'data_preferencial': data,
            'extensao': '.jpg'
        })()
        
        nome = generator_viagem.generate_filename(img, i)
        periodo = config_viagem.calculate_period_number(data)
        print(f"📅 {data.strftime('%d/%m/%Y')} -> Período {periodo:02d} -> {nome}")
    
    print()
    
    # 2. Configuração compatível (sistema anterior)
    print("2️⃣  SISTEMA COMPATÍVEL (BEBÊ)")
    print("-" * 30)
    config_bebe = ConfigurationManager.create_baby_configuration()
    
    datas_bebe = [
        datetime(2024, 8, 17),  # Nascimento
        datetime(2024, 10, 15), # Mês 02
        datetime(2025, 1, 20),  # Mês 05
    ]
    
    generator_bebe = FilenameGenerator(config_bebe)
    
    for i, data in enumerate(datas_bebe):
        img = type('MockImage', (), {
            'data_preferencial': data,
            'extensao': '.jpg'
        })()
        
        nome = generator_bebe.generate_filename(img, i)
        periodo = config_bebe.calculate_period_number(data)
        print(f"👶 {data.strftime('%d/%m/%Y')} -> Período {periodo:02d} -> {nome}")
    
    print()
    
    # 3. Configuração simples (apenas datas)
    print("3️⃣  PROJETO SIMPLES (SEM PERÍODOS)")
    print("-" * 30)
    config_simples = ConfigurationManager.create_custom_configuration(
        data_inicio=datetime(2023, 1, 1),
        prefixo="FOTO",
        incluir_periodo=False
    )
    
    data_simples = datetime(2023, 3, 15)
    generator_simples = FilenameGenerator(config_simples)
    
    img = type('MockImage', (), {
        'data_preferencial': data_simples,
        'extensao': '.png'
    })()
    
    nome = generator_simples.generate_filename(img, 0, {"15032023": "Aniversário"})
    print(f"📸 {data_simples.strftime('%d/%m/%Y')} -> {nome}")


def demo_flexibilidade():
    """Demonstra a flexibilidade do novo sistema."""
    print("\n🔧 DEMONSTRAÇÃO - FLEXIBILIDADE DO SISTEMA")
    print("=" * 60)
    
    # Diferentes formatos de nomenclatura
    configuracoes = [
        {
            'nome': 'Projeto Acadêmico',
            'config': ConfigurationManager.create_custom_configuration(
                data_inicio=datetime(2023, 9, 1),
                prefixo="PESQ",
                incluir_periodo=True
            )
        },
        {
            'nome': 'Evento Corporativo',
            'config': ConfigurationManager.create_custom_configuration(
                data_inicio=datetime(2023, 11, 15),
                prefixo="CORP",
                incluir_periodo=False
            )
        },
        {
            'nome': 'Álbum Familiar',
            'config': ConfigurationManager.create_custom_configuration(
                data_inicio=datetime(2023, 1, 1),
                prefixo="FAM",
                incluir_periodo=True
            )
        }
    ]
    
    data_exemplo = datetime(2023, 12, 25)
    
    for config_info in configuracoes:
        print(f"📁 {config_info['nome']}:")
        generator = FilenameGenerator(config_info['config'])
        
        img = type('MockImage', (), {
            'data_preferencial': data_exemplo,
            'extensao': '.jpg'
        })()
        
        nome = generator.generate_filename(img, 3, {"25122023": "Natal"})
        print(f"   🏷️  {nome}")
        print()


def demo_comparacao():
    """Compara sistema antigo vs novo."""
    print("⚖️  DEMONSTRAÇÃO - COMPARAÇÃO SISTEMAS")
    print("=" * 60)
    
    data_teste = datetime(2024, 9, 15)
    
    # Sistema antigo
    print("📰 SISTEMA ANTERIOR:")
    config_antigo = ConfigurationManager.create_baby_configuration()
    generator_antigo = FilenameGenerator(config_antigo)
    
    img = type('MockImage', (), {
        'data_preferencial': data_teste,
        'extensao': '.jpg'
    })()
    
    nome_antigo = generator_antigo.generate_filename(img, 1)
    print(f"   🏷️  {nome_antigo}")
    print("   📝 Características:")
    print("   ✓ Baseado em data fixa (17/08/2024)")
    print("   ✓ Prefixo fixo (MA 19a)")
    print("   ✓ Cálculo específico de mês do bebê")
    
    print()
    
    # Sistema novo
    print("🆕 SISTEMA NOVO:")
    config_novo = ConfigurationManager.create_custom_configuration(
        data_inicio=datetime(2024, 1, 1),
        prefixo="PROJ",
        incluir_periodo=True
    )
    generator_novo = FilenameGenerator(config_novo)
    
    nome_novo = generator_novo.generate_filename(img, 1)
    print(f"   🏷️  {nome_novo}")
    print("   📝 Características:")
    print("   ✓ Data de início configurável")
    print("   ✓ Prefixo personalizável")
    print("   ✓ Cálculo genérico de períodos")
    print("   ✓ Total flexibilidade")


if __name__ == "__main__":
    try:
        demo_configuracoes()
        demo_flexibilidade()
        demo_comparacao()
        
        print("\n" + "=" * 60)
        print("✨ RESUMO DAS PRINCIPAIS MELHORIAS:")
        print("=" * 60)
        print("🔧 1. Configuração totalmente personalizável")
        print("📅 2. Datas de início e fim flexíveis")
        print("🏷️  3. Prefixos customizáveis")
        print("📊 4. Cálculo de períodos genérico")
        print("🔄 5. Compatibilidade total com sistema anterior")
        print("🎯 6. Múltiplos projetos em paralelo")
        print("💡 7. Interface mais intuitiva")
        print()
        print("🎉 O sistema está pronto para uso em qualquer projeto!")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
