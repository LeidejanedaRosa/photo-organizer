
from datetime import datetime, timedelta
from typing import Optional

class ProjectConfiguration:
    
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
        
        self.data_inicio = data_inicio
        self.data_final = data_final
        self.prefixo_nomenclatura = prefixo_nomenclatura
        self.separador = separador
        self.incluir_periodo = incluir_periodo
        self.incluir_sequencial = incluir_sequencial
        self.formato_data = formato_data
    
    def calculate_period_number(self, data: datetime) -> int:
        
        if not self.incluir_periodo:
            return 0
            
        if data < self.data_inicio:
            return 0
        
        anos_diff = data.year - self.data_inicio.year
        meses_diff = anos_diff * 12 + (data.month - self.data_inicio.month)
        
        return self.data_inicio.day + meses_diff
    
    def calculate_year_number(self, data: datetime) -> int:
        
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
        
        if data < self.data_inicio:
            return False
        
        if self.data_final and data > self.data_final:
            return False
        
        return True
    
    def should_create_new_period(self, data: datetime) -> bool:
        
        if self.data_final and data > self.data_final:
            return True
        return False
    
    def suggest_new_period_config(
        self,
        data: datetime
    ) -> 'ProjectConfiguration':
        
        if not self.data_final:
            raise ValueError(
                "Não é possível sugerir novo período sem data final definida"
            )
        
        nova_data_inicio = self.data_final + timedelta(days=1)
        
        try:
            nova_data_final = (
                nova_data_inicio.replace(year=nova_data_inicio.year + 1) -
                timedelta(days=1)
            )
        except ValueError:
            
            nova_data_final = datetime(nova_data_inicio.year + 1, 2, 28)
        
        return ProjectConfiguration(
            data_inicio=nova_data_inicio,
            data_final=nova_data_final,
            prefixo_nomenclatura=self.prefixo_nomenclatura,
            separador=self.separador,
            incluir_periodo=self.incluir_periodo,
            incluir_sequencial=self.incluir_sequencial,
            formato_data=self.formato_data
        )
    
    def generate_filename_pattern(self, data: datetime, sequencial: int = 0, evento: Optional[str] = None) -> str:
        
        componentes = []
        
        if self.incluir_periodo:
            periodo = self.calculate_period_number(data)
            componentes.append(f"{periodo:02d}")
        
        if self.prefixo_nomenclatura:
            componentes.append(self.prefixo_nomenclatura)
        
        componentes.append(data.strftime(self.formato_data))
        
        nome_base = self.separador.join(componentes)
        
        if self.incluir_sequencial:
            nome_base += f"({sequencial:02d})"
        
        if evento:
            nome_base += f"{self.separador}{evento}"
        
        return nome_base

class ConfigurationManager:
    
    @staticmethod
    def create_custom_configuration(
        data_inicio: datetime,
        data_final: Optional[datetime] = None,
        prefixo: str = "IMG",
        incluir_periodo: bool = False
    ) -> ProjectConfiguration:
        
        if data_final is None:
            if data_inicio.month == 2 and data_inicio.day == 29:
                
                data_final = datetime(data_inicio.year + 1, 2, 28)
            else:
                try:
                    data_final = datetime(
                        data_inicio.year + 1,
                        data_inicio.month,
                        data_inicio.day - 1  
                    )
                except ValueError:
                    
                    data_final = datetime(
                        data_inicio.year + 1,
                        data_inicio.month,
                        28
                    )
        
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
        
        print("=" * 60)
        print("⚙️  CONFIGURAÇÃO PERSONALIZADA DO PROJETO")
        print("=" * 60)
        
        while True:
            try:
                data_str = input("📅 Data de início (DD/MM/AAAA): ").strip()
                data_inicio = datetime.strptime(data_str, "%d/%m/%Y")
                break
            except ValueError:
                print("❌ Data inválida. Use o formato DD/MM/AAAA")
        
        data_final_sugerida = data_inicio.replace(year=data_inicio.year + 1)
        data_final_sugerida = data_final_sugerida - timedelta(days=1)
        print(f"\n📅 Data final sugerida: "
              f"{data_final_sugerida.strftime('%d/%m/%Y')} (exato 1 ano)")
        
        data_final_input = input(
            "📅 Data final personalizada (DD/MM/AAAA) "
            "[Enter para usar sugerida]: "
        ).strip()
        
        data_final = None
        if data_final_input:
            try:
                data_final = datetime.strptime(data_final_input, "%d/%m/%Y")
                print(f"✅ Data final definida: "
                      f"{data_final.strftime('%d/%m/%Y')}")
            except ValueError:
                print("⚠️  Data final inválida, usando data sugerida")
        
        if not data_final:
            
            try:
                data_final = (
                    data_inicio.replace(year=data_inicio.year + 1) -
                    timedelta(days=1)
                )
            except ValueError:
                
                data_final = datetime(data_inicio.year + 1, 2, 28)
            print(f"✅ Data final automática: "
                  f"{data_final.strftime('%d/%m/%Y')}")
        
        prefixo_input = input(
            "\n🏷️  Prefixo da nomenclatura [Enter para 'IMG']: "
        ).strip()
        prefixo = prefixo_input if prefixo_input else "IMG"
        
        print("\n📊 NUMERAÇÃO SEQUENCIAL:")
        print("   ✅ COM números: 00-FOTO-data, 01-FOTO-data (cronológica)")
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