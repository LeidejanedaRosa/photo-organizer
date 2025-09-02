
from datetime import datetime, timedelta
from typing import Optional

class ProjectConfiguration:
    
    def __init__(
        self,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        naming_prefix: str = "IMG",
        separador: str = " - ",
        include_period: bool = True,
        include_sequential: bool = True,
        date_format: str = "%d%m%Y"
    ):
        
        self.start_date = start_date
        self.end_date = end_date
        self.naming_prefix = naming_prefix
        self.separador = separador
        self.include_period = include_period
        self.include_sequential = include_sequential
        self.date_format = date_format
    
    def calculate_period_number(self, date: datetime) -> int:
        
        if not self.include_period:
            return 0
            
        if date < self.start_date:
            return 0
        
        anos_diff = date.year - self.start_date.year
        meses_diff = anos_diff * 12 + (date.month - self.start_date.month)
        
        return self.start_date.day + meses_diff
    
    def calculate_year_number(self, date: datetime) -> int:
        
        if not self.include_period:
            return 0
            
        if date < self.start_date:
            return 0
        
        anos_passados = date.year - self.start_date.year
        aniversario_atual = datetime(
            date.year, 
            self.start_date.month, 
            self.start_date.day
        )
        
        if date >= aniversario_atual:
            return anos_passados + 1
        else:
            return anos_passados if anos_passados > 0 else 1
    
    def is_date_in_range(self, date: datetime) -> bool:
        
        if date < self.start_date:
            return False
        
        if self.end_date and date > self.end_date:
            return False
        
        return True
    
    def should_create_new_period(self, date: datetime) -> bool:
        
        if self.end_date and date > self.end_date:
            return True
        return False
    
    def suggest_new_period_config(
        self,
        date: datetime
    ) -> 'ProjectConfiguration':
        
        if not self.end_date:
            raise ValueError(
                "Não é possível sugerir novo período sem date final definida"
            )
        
        nova_data_inicio = self.end_date + timedelta(days=1)
        
        try:
            nova_data_final = (
                nova_data_inicio.replace(year=nova_data_inicio.year + 1) -
                timedelta(days=1)
            )
        except ValueError:
            
            nova_data_final = datetime(nova_data_inicio.year + 1, 2, 28)
        
        return ProjectConfiguration(
            start_date=nova_data_inicio,
            end_date=nova_data_final,
            naming_prefix=self.naming_prefix,
            separador=self.separador,
            include_period=self.include_period,
            include_sequential=self.include_sequential,
            date_format=self.date_format
        )
    
    def generate_filename_pattern(self, date: datetime, sequential: int = 0, evento: Optional[str] = None) -> str:
        
        componentes = []
        
        if self.include_period:
            period = self.calculate_period_number(date)
            componentes.append(f"{period:02d}")
        
        if self.naming_prefix:
            componentes.append(self.naming_prefix)
        
        componentes.append(date.strftime(self.date_format))
        
        nome_base = self.separador.join(componentes)
        
        if self.include_sequential:
            nome_base += f"({sequential:02d})"
        
        if evento:
            nome_base += f"{self.separador}{evento}"
        
        return nome_base

class ConfigurationManager:
    
    @staticmethod
    def create_custom_configuration(
        start_date: datetime,
        end_date: Optional[datetime] = None,
        prefix: str = "IMG",
        include_period: bool = False
    ) -> ProjectConfiguration:
        
        if end_date is None:
            if start_date.month == 2 and start_date.day == 29:
                
                end_date = datetime(start_date.year + 1, 2, 28)
            else:
                try:
                    end_date = datetime(
                        start_date.year + 1,
                        start_date.month,
                        start_date.day - 1  
                    )
                except ValueError:
                    
                    end_date = datetime(
                        start_date.year + 1,
                        start_date.month,
                        28
                    )
        
        return ProjectConfiguration(
            start_date=start_date,
            end_date=end_date,
            naming_prefix=prefix,
            separador=" - ",
            include_period=include_period,
            include_sequential=True,
            date_format="%d%m%Y"
        )
    
    @staticmethod
    def prompt_user_configuration() -> ProjectConfiguration:
        
        print("=" * 60)
        print("⚙️  CONFIGURAÇÃO PERSONALIZADA DO PROJETO")
        print("=" * 60)
        
        while True:
            try:
                data_str = input("📅 Data de início (DD/MM/AAAA): ").strip()
                start_date = datetime.strptime(data_str, "%d/%m/%Y")
                break
            except ValueError:
                print("❌ Data inválida. Use o formato DD/MM/AAAA")
        
        data_final_sugerida = start_date.replace(year=start_date.year + 1)
        data_final_sugerida = data_final_sugerida - timedelta(days=1)
        print(f"\n📅 Data final sugerida: "
              f"{data_final_sugerida.strftime('%d/%m/%Y')} (exato 1 ano)")
        
        data_final_input = input(
            "📅 Data final personalizada (DD/MM/AAAA) "
            "[Enter para usar sugerida]: "
        ).strip()
        
        end_date = None
        if data_final_input:
            try:
                end_date = datetime.strptime(data_final_input, "%d/%m/%Y")
                print(f"✅ Data final definida: "
                      f"{end_date.strftime('%d/%m/%Y')}")
            except ValueError:
                print("⚠️  Data final inválida, usando date sugerida")
        
        if not end_date:
            
            try:
                end_date = (
                    start_date.replace(year=start_date.year + 1) -
                    timedelta(days=1)
                )
            except ValueError:
                
                end_date = datetime(start_date.year + 1, 2, 28)
            print(f"✅ Data final automática: "
                  f"{end_date.strftime('%d/%m/%Y')}")
        
        prefixo_input = input(
            "\n🏷️  Prefixo da nomenclatura [Enter para 'IMG']: "
        ).strip()
        prefix = prefixo_input if prefixo_input else "IMG"
        
        print("\n📊 NUMERAÇÃO SEQUENCIAL:")
        print("   ✅ COM números: 00-FOTO-date, 01-FOTO-date (cronológica)")
        print("   ❌ SEM números: FOTO-date (ordem alfabética quebrada)")
        incluir_periodo_input = input(
            "📊 Incluir numeração sequential? (S/n): "
        ).strip().lower()
        include_period = incluir_periodo_input not in [
            'n', 'nao', 'no', 'não'
        ]
        
        print("\n✅ Configuração criada com sucesso!")
        print(f"   📅 Período: {start_date.strftime('%d/%m/%Y')}", end="")
        if end_date:
            print(f" até {end_date.strftime('%d/%m/%Y')}")
        else:
            print(" (sem date final)")
        print(f"   🏷️  Prefixo: {prefix}")
        print(f"   📊 Período: {'Sim' if include_period else 'Não'}")
        print()
        
        return ProjectConfiguration(
            start_date=start_date,
            end_date=end_date,
            naming_prefix=prefix,
            separador=" - ",
            include_period=include_period,
            include_sequential=True,
            date_format="%d%m%Y"
        )