import os
from typing import Optional


class MenuController:
    """Responsável por exibir menus e capturar entradas do usuário."""
    
    @staticmethod
    def exibir_menu_inteligente(tem_fotos_organizadas: bool, tem_configuracao: bool) -> int:
        """Exibe menu adaptativo baseado no estado atual do sistema."""
        print("=" * 70)
        print("🖼️  ORGANIZADOR DE FOTOS  🖼️")
        print("=" * 70)
        print()
        
        if not tem_fotos_organizadas:
            # Menu para primeiro acesso ou pastas não organizadas
            print("� PRIMEIROS PASSOS:")
            print("   1️⃣  Configurar como nomear suas fotos")
            print("   2️⃣  Remover fotos duplicadas")  
            print("   3️⃣  Organizar fotos em ordem cronológica")
            print("   4️⃣  Fazer tudo (duplicatas + renomeação)")
            print()
            print("📊 INFORMAÇÕES:")
            print("   5️⃣  Ver relatório das suas fotos")
            opcoes_validas = ['1', '2', '3', '4', '5']
            max_opcao = 5
        else:
            # Menu completo para pastas já organizadas
            print("🔧 ORGANIZAÇÃO:")
            print("   1️⃣  Configurar nomenclatura das fotos")
            print("   2️⃣  Remover fotos duplicadas")
            print("   3️⃣  Organizar fotos em ordem cronológica") 
            print("   4️⃣  Fazer tudo (duplicatas + renomeação)")
            print()
            print("📁 ORGANIZAR EM PASTAS:")
            print("   5️⃣  Criar pastas por eventos nas fotos")
            print("   6️⃣  Criar pastas por períodos personalizados")
            print()
            print("🔍 BUSCA E RELATÓRIOS:")
            print("   7️⃣  Buscar fotos por período específico")
            print("   8️⃣  Ver relatório detalhado")
            print()
            print("💾 BACKUP:")
            print("   9️⃣  Criar backup do estado atual")
            opcoes_validas = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            max_opcao = 9
        
        print("=" * 70)
        
        while True:
            try:
                opcao = input(f"\n🔢 Escolha uma opção (1-{max_opcao}): ").strip()
                if opcao in opcoes_validas:
                    return int(opcao)
                else:
                    print(f"❌ Opção inválida! Digite um número de 1 a {max_opcao}.")
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
