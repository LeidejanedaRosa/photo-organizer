#!/usr/bin/env python3
"""
Teste da funcionalidade de cálculo do ano do bebê
"""
from datetime import datetime

def calcular_ano_bebe(data: datetime) -> int:
    """
    Calcula qual ano do bebê baseado na data da foto.
    Ano 1: 01/01/2025 a 31/12/2025
    Ano 2: 17/08/2025 a 16/08/2026
    E assim por diante...
    """
    # Data de nascimento base: 01/01/2025
    data_nascimento = datetime(2024, 8, 17)
    
    # Se a foto é antes do nascimento, retorna 0 (inválido)
    if data < data_nascimento:
        return 0
    
    # Calcula a diferença em anos
    anos_passados = data.year - data_nascimento.year
    
    # Verifica se já passou o aniversário no ano atual
    aniversario_atual = datetime(data.year, 8, 17)
    
    if data >= aniversario_atual:
        # Já passou o aniversário este ano
        return anos_passados + 1
    else:
        # Ainda não chegou o aniversário este ano
        return anos_passados

def calcular_mes_bebe(data: datetime) -> int:
    """Calcula o mês do bebê baseado na data da foto."""
    mes = data.month
    dia = data.day
    
    # Se estamos em agosto
    if mes == 8:
        # Se é depois ou igual a 17/08
        if dia >= 17:
            return 0  # Mês 00
        else:
            return 12  # Mês 12 (primeira parte de agosto)
    
    # Para outros meses
    if mes >= 9:  # Setembro a dezembro
        return mes - 8  # 9-8=1 (setembro), 10-8=2 (outubro), etc.
    else:  # Janeiro a julho
        return mes + 4  # 1+4=5 (janeiro), 2+4=6 (fevereiro), etc.

if __name__ == "__main__":
    # Teste das funções
    print("🧪 TESTANDO AS FUNÇÕES DE CÁLCULO")
    print("=" * 50)
    
    datas_teste = [
        datetime(2024, 8, 17),   # Nascimento - Ano 1, Mês 00
        datetime(2024, 9, 15),   # Ano 1, Mês 01
        datetime(2025, 1, 10),   # Ano 1, Mês 05
        datetime(2025, 8, 10),   # Ano 1, Mês 12
        datetime(2025, 8, 17),   # Ano 2, Mês 00
        datetime(2025, 9, 15),   # Ano 2, Mês 01
        datetime(2026, 8, 16),   # Ano 2, Mês 12
        datetime(2026, 8, 17),   # Ano 3, Mês 00
    ]
    
    for data in datas_teste:
        ano = calcular_ano_bebe(data)
        mes = calcular_mes_bebe(data)
        print(f"📅 {data.strftime('%d/%m/%Y')} -> Ano {ano}, Mês {mes:02d}")
    
    print("=" * 50)
    print("✅ Teste concluído!")
