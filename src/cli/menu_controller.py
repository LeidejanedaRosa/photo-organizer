import os
from typing import Optional


class MenuController:
    """Responsável por exibir menus e capturar entradas do usuário."""
    
    @staticmethod
    def exibir_menu_inicial() -> int:
        """Exibe um menu inicial bonito e retorna a opção escolhida."""
        print("=" * 70)
        print("🖼️  ORGANIZADOR DE FOTOS  🖼️")
        print("=" * 70)
        print()
        print("📋 FUNCIONALIDADES DISPONÍVEIS:")
        print("   1️⃣  Detectar e mover duplicatas")
        print("   2️⃣  Ordenar fotos por data")
        print("   3️⃣  Fazer tudo (duplicatas + ordenação)")
        print("   4️⃣  Relatório detalhado")
        print("   5️⃣  Buscar fotos por período")
        print("   6️⃣  Organizar por eventos")
        print("   7️⃣  Organizar por períodos customizados")
        print("   8️⃣  Criar backup do estado atual")
        print("   9️⃣  Como você quer nomear suas fotos?")
        print()
        print("🎯 NOMENCLATURA CONFIGURÁVEL:")
        print("   📅 Sistema flexível - configure suas preferências")
        print("   📝 Padrão compatível com sistema anterior disponível")
        print("   🗓️ Períodos e datas totalmente personalizáveis")
        print()
        print("=" * 70)
        
        while True:
            try:
                opcao = input("\n🔢 Escolha uma opção (1-9): ").strip()
                if opcao in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    return int(opcao)
                else:
                    print("❌ Opção inválida! Digite um número de 1 a 9.")
            except KeyboardInterrupt:
                print("\n\n👋 Operação cancelada pelo usuário.")
                exit(0)
    
    @staticmethod
    def solicitar_diretorio() -> str:
        """Solicita o diretório das fotos."""
        print("\n📁 CONFIGURAÇÃO DO DIRETÓRIO:")
        
        while True:
            caminho = input("📁 Digite o caminho do diretório: ").strip()
            if caminho and os.path.exists(caminho):
                return caminho
            elif not caminho:
                print("❌ Por favor, digite um caminho válido!")
            else:
                print("❌ Diretório não encontrado! Tente novamente.")
    
    @staticmethod
    def confirmar_operacao(mensagem: str) -> bool:
        """Solicita confirmação do usuário para uma operação."""
        resposta = input(f"\n❓ {mensagem} (s/N): ").strip().lower()
        return resposta == 's'
    
    @staticmethod
    def solicitar_periodo() -> tuple[str, str]:
        """Solicita período de datas do usuário."""
        print("📅 Digite o período desejado:")
        data_inicio = input("   📆 Data início (DD/MM/AAAA): ").strip()
        data_fim = input("   📆 Data fim (DD/MM/AAAA): ").strip()
        return data_inicio, data_fim
    
    @staticmethod
    def imprimir_separador(titulo: Optional[str] = None) -> None:
        """Imprime um separador visual."""
        print("\n" + "=" * 70)
        if titulo:
            print(titulo)
            print("=" * 70)
    
    @staticmethod
    def imprimir_conclusao() -> None:
        """Imprime mensagem de conclusão."""
        print("\n" + "=" * 70)
        print("✅ OPERAÇÃO CONCLUÍDA!")
        print("=" * 70)
