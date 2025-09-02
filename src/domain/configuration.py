from datetime import datetime, timedelta
from typing import Optional


class ProjectConfiguration:

    def __init__(
        self,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        naming_prefix: str = "IMG",
        separator: str = " - ",
        include_period: bool = True,
        include_sequential: bool = True,
        date_format: str = "%d%m%Y",
    ):

        self.start_date = start_date
        self.end_date = end_date
        self.naming_prefix = naming_prefix
        self.separator = separator
        self.include_period = include_period
        self.include_sequential = include_sequential
        self.date_format = date_format

    def calculate_period_number(self, date: datetime) -> int:

        if not self.include_period:
            return 0

        if date < self.start_date:
            return 0

        years_diff = date.year - self.start_date.year
        months_diff = years_diff * 12 + (date.month - self.start_date.month)

        return self.start_date.day + months_diff

    def calculate_year_number(self, date: datetime) -> int:

        if not self.include_period:
            return 0

        if date < self.start_date:
            return 0

        years_past = date.year - self.start_date.year
        current_birthday = datetime(
            date.year, self.start_date.month, self.start_date.day
        )

        if date >= current_birthday:
            return years_past + 1
        else:
            return years_past if years_past > 0 else 1

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

    def suggest_new_period_config(self) -> "ProjectConfiguration":

        if not self.end_date:
            raise ValueError(
                "Não é possível sugerir novo período sem data final definida"
            )

        new_start_date = self.end_date + timedelta(days=1)

        try:
            new_end_date = new_start_date.replace(
                year=new_start_date.year + 1
            ) - timedelta(days=1)
        except ValueError:

            new_end_date = datetime(new_start_date.year + 1, 2, 28)

        return ProjectConfiguration(
            start_date=new_start_date,
            end_date=new_end_date,
            naming_prefix=self.naming_prefix,
            separator=self.separator,
            include_period=self.include_period,
            include_sequential=self.include_sequential,
            date_format=self.date_format,
        )

    def generate_filename_pattern(
        self, date: datetime, sequential: int = 0, event: Optional[str] = None
    ) -> str:

        components = []

        if self.include_period:
            period = self.calculate_period_number(date)
            components.append(f"{period:02d}")

        if self.naming_prefix:
            components.append(self.naming_prefix)

        components.append(date.strftime(self.date_format))

        base_name = self.separator.join(components)

        if self.include_sequential:
            base_name += f"({sequential:02d})"

        if event:
            base_name += f"{self.separator}{event}"

        return base_name


class ConfigurationManager:

    @staticmethod
    def create_custom_configuration(
        start_date: datetime,
        end_date: Optional[datetime] = None,
        prefix: str = "IMG",
        include_period: bool = False,
    ) -> ProjectConfiguration:

        if end_date is None:
            if start_date.month == 2 and start_date.day == 29:

                end_date = datetime(start_date.year + 1, 2, 28)
            else:
                try:
                    end_date = datetime(
                        start_date.year + 1,
                        start_date.month,
                        start_date.day - 1,
                    )
                except ValueError:

                    end_date = datetime(
                        start_date.year + 1, start_date.month, 28
                    )

        return ProjectConfiguration(
            start_date=start_date,
            end_date=end_date,
            naming_prefix=prefix,
            separator=" - ",
            include_period=include_period,
            include_sequential=True,
            date_format="%d%m%Y",
        )

    @staticmethod
    def prompt_user_configuration() -> ProjectConfiguration:

        print("=" * 60)
        print("⚙️  CONFIGURAÇÃO PERSONALIZADA DO PROJETO")
        print("=" * 60)

        while True:
            try:
                date_str = input("📅 Data de início (DD/MM/AAAA): ").strip()
                start_date = datetime.strptime(date_str, "%d/%m/%Y")
                break
            except ValueError:
                print("❌ Data inválida. Use o formato DD/MM/AAAA")

        suggested_end_date = start_date.replace(year=start_date.year + 1)
        suggested_end_date = suggested_end_date - timedelta(days=1)
        print(
            f"\n📅 Data final sugerida: "
            f"{suggested_end_date.strftime('%d/%m/%Y')} (exato 1 ano)"
        )

        final_input_date = input(
            "📅 Data final personalizada (DD/MM/AAAA) "
            "[Enter para usar sugerida]: "
        ).strip()

        end_date = None
        if final_input_date:
            try:
                end_date = datetime.strptime(final_input_date, "%d/%m/%Y")
                print(
                    f"✅ Data final definida: "
                    f"{end_date.strftime('%d/%m/%Y')}"
                )
            except ValueError:
                print("⚠️  Data final inválida, usando date sugerida")

        if not end_date:

            try:
                end_date = start_date.replace(
                    year=start_date.year + 1
                ) - timedelta(days=1)
            except ValueError:

                end_date = datetime(start_date.year + 1, 2, 28)
            print(
                f"✅ Data final automática: "
                f"{end_date.strftime('%d/%m/%Y')}"
            )

        prefix_input = input(
            "\n🏷️  prefix da nomenclatura [Enter para 'IMG']: "
        ).strip()
        prefix = prefix_input if prefix_input else "IMG"

        print("\n📊 NUMERAÇÃO SEQUENCIAL:")
        print("   ✅ COM números: 00-FOTO-date, 01-FOTO-date (cronológica)")
        print("   ❌ SEM números: FOTO-date (ordem cronológica quebrada)")
        include_period_input = (
            input("📊 Incluir numeração sequencial? (S/n): ").strip().lower()
        )
        include_period = include_period_input not in ["n", "nao", "no", "não"]

        print("\n✅ Configuração criada com sucesso!")
        print(f"   📅 Período: {start_date.strftime('%d/%m/%Y')}", end="")
        if end_date:
            print(f" até {end_date.strftime('%d/%m/%Y')}")
        else:
            print(" (sem data final)")
        print(f"   🏷️ Prefixo: {prefix}")
        print(f"   📊 Período: {'Sim' if include_period else 'Não'}")
        print()

        return ProjectConfiguration(
            start_date=start_date,
            end_date=end_date,
            naming_prefix=prefix,
            separator=" - ",
            include_period=include_period,
            include_sequential=True,
            date_format="%d%m%Y",
        )
