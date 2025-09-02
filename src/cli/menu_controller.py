import os
from typing import Optional, Tuple


class MenuController:

    @staticmethod
    def display_smart_menu(
        has_organized_photos: bool, has_configuration: bool
    ) -> int:

        print("=" * 70)
        print("🖼️  ORGANIZADOR DE FOTOS  🖼️")
        print("=" * 70)
        print()

        if not has_organized_photos:

            print("� PRIMEIROS PASSOS:")
            print("   1️⃣  Configurar como nomear suas fotos")
            print("   2️⃣  Remover fotos duplicadas")
            print("   3️⃣  Organizar fotos em ordem cronológica")
            print("   4️⃣  Fazer tudo (duplicatas + renomeação)")
            print()
            print("📊 INFORMAÇÕES:")
            print("   5️⃣  Ver relatório das suas fotos")
            valid_options = ["1", "2", "3", "4", "5"]
            max_option = 5
        else:

            print("🔧 ORGANIZAÇÃO:")
            if has_configuration:
                print("   1️⃣  Reconfigurar nomenclatura das fotos")
            else:
                print("   1️⃣  Configurar nomenclatura das fotos")
            print("   2️⃣  Remover fotos duplicadas")
            print("   3️⃣  Organizar fotos em ordem cronológica")
            print("   4️⃣  Fazer tudo (duplicatas + renomeação)")
            print()
            print("📁 ORGANIZAR EM PASTAS:")
            print("   5️⃣  Criar pastas por events nas fotos")
            print("   6️⃣  Criar pastas por períodos personalizados")
            print()
            print("🔍 BUSCA E RELATÓRIOS:")
            print("   7️⃣  Buscar fotos por período específico")
            print("   8️⃣  Ver relatório detalhado")
            print()
            print("💾 BACKUP:")
            print("   9️⃣  Criar backup do estado atual")
            valid_options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            max_option = 9

        print("=" * 70)

        while True:
            try:
                option = input(
                    f"\n🔢 Escolha uma opção (1-{max_option}): "
                ).strip()
                if option in valid_options:
                    return int(option)
                else:
                    print(
                        f"❌ Opção inválida! Digite um número de 1 a {max_option}."
                    )
            except KeyboardInterrupt:
                print("\n\n👋 Operação cancelada pelo usuário.")
                exit(0)

    @staticmethod
    def request_directory() -> str:

        print("\n📁 CONFIGURAÇÃO DO DIRETÓRIO:")

        while True:
            path = input("📁 Digite o caminho do diretório: ").strip()
            if path and os.path.exists(path):
                return path
            elif not path:
                print("❌ Por favor, digite um caminho válido!")
            else:
                print("❌ Diretório não encontrado! Tente novamente.")

    @staticmethod
    def confirm_operation(message: str) -> bool:

        response = input(f"\n❓ {message} (s/N): ").strip().lower()
        return response == "s"

    @staticmethod
    def request_period() -> Tuple[str, str]:

        print("📅 Digite o período desejado:")
        start_date = input("   📆 Data início (DD/MM/AAAA): ").strip()
        end_date = input("   📆 Data fim (DD/MM/AAAA): ").strip()
        return start_date, end_date

    @staticmethod
    def print_separator(title: Optional[str] = None) -> None:

        print("\n" + "=" * 70)
        if title:
            print(title)
            print("=" * 70)

    @staticmethod
    def print_conclusion() -> None:

        print("\n" + "=" * 70)
        print("✅ OPERAÇÃO CONCLUÍDA!")
        print("=" * 70)
