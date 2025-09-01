"""
Módulo para configurações personalizáveis do organizador de fotos.
"""
from datetime import datetime
from typing import Optional


class ProjectConfiguration:
    """
    Configuração do projeto de organização de fotos.
    Permite personalizar datas, nomenclatura e outros parâmetros.
    """
    
    def __init__(
        self,
        data_inicio: datetime,
        data_final: Optional[datetime] = None,
        prefixo_nomenclatura: str = "IMG",
        separador: str = " - ",
        incluir_periodo: bool = True,
        incluir_sequencial: bool = True,
        formato_data: str = "%d%m%Y"
    ):
        """
        Inicializa a configuração do projeto.
        
        Args:
            data_inicio: Data de início do projeto/período
            data_final: Data final do projeto (opcional)
            prefixo_nomenclatura: Prefixo para nomenclatura (ex: "IMG", "IMG", etc)
            separador: Separador entre elementos do nome
            incluir_periodo: Se deve incluir cálculo de período (mês/ano)
            incluir_sequencial: Se deve incluir numeração sequencial
            formato_data: Formato da data no nome do arquivo
        """
        self.data_inicio = data_inicio
        self.data_final = data_final
        self.prefixo_nomenclatura = prefixo_nomenclatura
        self.separador = separador
        self.incluir_periodo = incluir_periodo
        self.incluir_sequencial = incluir_sequencial
        self.formato_data = formato_data
    
    def calculate_period_number(self, data: datetime) -> int:
        """
        Calcula o número do período baseado na data da foto.
        
        Sistema de ano fiscal personalizado:
        - Período 00: Do dia inicial até final do primeiro mês
        - Períodos seguintes: Meses completos em sequência
        
        Exemplo: Início 08/03/2025
        - 08/03 a 31/03/2025 = período 00
        - 01/04 a 30/04/2025 = período 01  
        - 01/05 a 31/05/2025 = período 02
        - etc.
        """
        if not self.incluir_periodo:
            return 0
            
        if data < self.data_inicio:
            return 0
        
        # Calcula diferença em meses calendário
        anos_diff = data.year - self.data_inicio.year
        meses_diff = anos_diff * 12 + (data.month - self.data_inicio.month)
        
        return meses_diff
    
    def calculate_year_number(self, data: datetime) -> int:
        """
        Calcula o ano do período baseado na data da foto.
        """
        if not self.incluir_periodo:
            return 0
            
        if data < self.data_inicio:
            return 0
        
        anos_passados = data.year - self.data_inicio.year
        aniversario_atual = datetime(
            data.year, 
            self.data_inicio.month, 
            self.data_inicio.day
        )
        
        if data >= aniversario_atual:
            return anos_passados + 1
        else:
            return anos_passados if anos_passados > 0 else 1
    
    def is_date_in_range(self, data: datetime) -> bool:
        """Verifica se a data está dentro do período configurado."""
        if data < self.data_inicio:
            return False
        
        if self.data_final and data > self.data_final:
            return False
        
        return True
    
    def generate_filename_pattern(self, data: datetime, sequencial: int = 0, evento: Optional[str] = None) -> str:
        """
        Gera o padrão de nomenclatura baseado na configuração.
        
        Args:
            data: Data da foto
            sequencial: Número sequencial
            evento: Descrição do evento (opcional)
        
        Returns:
            String com o padrão de nomenclatura
        """
        componentes = []
        
        # Adiciona período se configurado
        if self.incluir_periodo:
            periodo = self.calculate_period_number(data)
            componentes.append(f"{periodo:02d}")
        
        # Adiciona prefixo
        if self.prefixo_nomenclatura:
            componentes.append(self.prefixo_nomenclatura)
        
        # Adiciona data
        componentes.append(data.strftime(self.formato_data))
        
        # Junta componentes com separador
        nome_base = self.separador.join(componentes)
        
        # Adiciona sequencial se configurado
        if self.incluir_sequencial:
            nome_base += f"({sequencial:02d})"
        
        # Adiciona evento se fornecido
        if evento:
            nome_base += f"{self.separador}{evento}"
        
        return nome_base


class ConfigurationManager:
    """Gerenciador de configurações do projeto."""
    
    @staticmethod
    def create_baby_configuration() -> ProjectConfiguration:
        """
        Cria uma configuração compatível com o sistema anterior (bebê).
        Mantém compatibilidade com nomenclatura existente.
        """
        return ProjectConfiguration(
            data_inicio=datetime(2024, 8, 17),
            prefixo_nomenclatura="IMG",
            separador=" - ",
            incluir_periodo=True,
            incluir_sequencial=True,
            formato_data="%d%m%Y"
        )
    
    @staticmethod
    def create_custom_configuration(
        data_inicio: datetime,
        data_final: Optional[datetime] = None,
        prefixo: str = "IMG",
        incluir_periodo: bool = False
    ) -> ProjectConfiguration:
        """
        Cria uma configuração personalizada.
        """
        return ProjectConfiguration(
            data_inicio=data_inicio,
            data_final=data_final,
            prefixo_nomenclatura=prefixo,
            separador=" - ",
            incluir_periodo=incluir_periodo,
            incluir_sequencial=True,
            formato_data="%d%m%Y"
        )
    
    @staticmethod
    def prompt_user_configuration() -> ProjectConfiguration:
        """
        Solicita configuração personalizada do usuário via input.
        """
        print("=" * 60)
        print("⚙️  CONFIGURAÇÃO PERSONALIZADA DO PROJETO")
        print("=" * 60)
        
        # Data de início
        while True:
            try:
                data_str = input("📅 Data de início (DD/MM/AAAA): ").strip()
                data_inicio = datetime.strptime(data_str, "%d/%m/%Y")
                break
            except ValueError:
                print("❌ Data inválida. Use o formato DD/MM/AAAA")
        
        # Data final (opcional)
        data_final = None
        data_final_input = input("📅 Data final (DD/MM/AAAA) [opcional, Enter para pular]: ").strip()
        if data_final_input:
            try:
                data_final = datetime.strptime(data_final_input, "%d/%m/%Y")
            except ValueError:
                print("⚠️  Data final inválida, será ignorada")
        
        # Prefixo da nomenclatura
        prefixo = input("🏷️  Prefixo da nomenclatura (ex: 'IMG', 'FOTO'): ").strip()
        if not prefixo:
            prefixo = "IMG"
        
        # Incluir cálculo de período
        print("\n📊 NUMERAÇÃO SEQUENCIAL:")
        print("   ✅ COM números: 00-FOTO-data, 01-FOTO-data (ordem cronológica)")
        print("   ❌ SEM números: FOTO-data (ordem alfabética quebrada)")
        incluir_periodo_input = input(
            "📊 Incluir numeração sequencial? (S/n): "
        ).strip().lower()
        incluir_periodo = incluir_periodo_input not in [
            'n', 'nao', 'no', 'não'
        ]
        
        print("\n✅ Configuração criada com sucesso!")
        print(f"   📅 Período: {data_inicio.strftime('%d/%m/%Y')}", end="")
        if data_final:
            print(f" até {data_final.strftime('%d/%m/%Y')}")
        else:
            print(" (sem data final)")
        print(f"   🏷️  Prefixo: {prefixo}")
        print(f"   📊 Período: {'Sim' if incluir_periodo else 'Não'}")
        print()
        
        return ProjectConfiguration(
            data_inicio=data_inicio,
            data_final=data_final,
            prefixo_nomenclatura=prefixo,
            separador=" - ",
            incluir_periodo=incluir_periodo,
            incluir_sequencial=True,
            formato_data="%d%m%Y"
        )
