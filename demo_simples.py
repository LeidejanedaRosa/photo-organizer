#!/usr/bin/env python3
"""
Demonstração das funcionalidades do Organizador de Fotos v2.0
"""
from datetime import datetime
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.domain.configuration import ConfigurationManager


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
    
    print(f"📅 Data início: {config_viagem.data_inicio.strftime('%d/%m/%Y')}")
    print(f"📅 Data fim: {config_viagem.data_final.strftime('%d/%m/%Y')}")
    print(f"🏷️  Prefixo: {config_viagem.prefixo_nomenclatura}")
    print(f"📊 Período: {'Sim' if config_viagem.incluir_periodo else 'Não'}")
    print()
    
    # 2. Configuração simples
    print("2️⃣  PROJETO SIMPLES")
    print("-" * 30)
    config_simples = ConfigurationManager.create_custom_configuration(
        data_inicio=datetime(2023, 1, 1),
        prefixo="FOTO",
        incluir_periodo=False
    )
    
    print(f"📅 Data início: {config_simples.data_inicio.strftime('%d/%m/%Y')}")
    print(f"🏷️  Prefixo: {config_simples.prefixo_nomenclatura}")
    print(f"📊 Período: {'Sim' if config_simples.incluir_periodo else 'Não'}")
    
    print("\n✅ Demonstração das configurações concluída")


if __name__ == "__main__":
    demo_configuracoes()
