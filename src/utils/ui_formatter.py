from typing import Any, Dict


class UIFormatter:

    SEPARATOR_THIN = "─" * 50
    SEPARATOR_MEDIUM = "─" * 60
    SEPARATOR_THICK = "─" * 70

    @staticmethod
    def print_operation_header(operation_name: str, simulate: bool = True):

        mode = "🔄 SIMULAÇÃO" if simulate else "📁 EXECUTANDO"
        print(f"\n{mode}: {operation_name}...")

    @staticmethod
    def print_separator(width: int = 70):

        print("─" * width)

    @staticmethod
    def print_operation_result(
        operation_name: str,
        count: int,
        item_type: str = "itens",
        simulate: bool = True,
    ):

        UIFormatter.print_separator()
        if simulate:
            print(f"📊 PREVISÃO: {count} {item_type} seriam processados")
        else:
            print(f"📊 RESULTADO: {count} {item_type} processados")
        UIFormatter.print_separator()

    @staticmethod
    def print_group_header(
        group_name: str, count: int, item_type: str = "itens"
    ):

        print(f"\n📂 {group_name}")
        print(f"   📊 {count} {item_type} encontrado(s)")

    @staticmethod
    def print_stats_summary(stats: Dict[str, Any]):

        print("\n📊 RESUMO:")
        for key, value in stats.items():
            print(f"   {key}: {value}")

    @staticmethod
    def validate_list_not_empty(items, empty_message: str) -> bool:

        if not items:
            print(f"✅ {empty_message}")
            return False
        return True
