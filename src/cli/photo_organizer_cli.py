from typing import List

from ..domain.image import ImageInfo, PeriodCalculator
from ..domain.configuration import ProjectConfiguration, ConfigurationManager
from ..services.photo_organizer_service import PhotoOrganizerService
from ..utils.event_manager import EventManager
from .menu_controller import MenuController


class PhotoOrganizerCLI:
    """
    Interface de linha de comando para o organizador de fotos.
    Segue o princípio de Responsabilidade Única - apenas interface.
    """
    
    def __init__(self):
        self.service = PhotoOrganizerService()
        self.menu = MenuController()
        self.configuration = None  # Será definida pelo usuário
    
    def run(self) -> None:
        """Executa a aplicação CLI."""
        try:
            opcao = self.menu.exibir_menu_inicial()
            diretorio = self.menu.solicitar_diretorio()
            self._executar_opcao(opcao, diretorio)
        except KeyboardInterrupt:
            print("\n\n👋 Programa encerrado pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("🔧 Verifique o diretório e tente novamente.")
    
    def _executar_opcao(self, opcao: int, diretorio: str) -> None:
        """Executa a opção escolhida pelo usuário."""
        self.menu.imprimir_separador()
        
        # Para opção 9, configura primeiro
        if opcao == 9:
            self._opcao_configuracao_personalizada()
            return
        
        # Análise inicial do diretório
        imagens_nao_org, imagens_org = self.service.analyze_directory(diretorio)
        todas_imagens = imagens_nao_org + imagens_org
        
        if opcao == 1:
            self._opcao_duplicatas(todas_imagens, diretorio)
        elif opcao == 2:
            self._opcao_renomear(imagens_nao_org, diretorio)
        elif opcao == 3:
            self._opcao_processo_completo(
                imagens_nao_org, imagens_org, diretorio
            )
        elif opcao == 4:
            self._opcao_relatorio(todas_imagens)
        elif opcao == 5:
            self._opcao_buscar_periodo(todas_imagens)
        elif opcao == 6:
            self._opcao_organizar_eventos(todas_imagens, diretorio)
        elif opcao == 7:
            self._opcao_organizar_periodos_customizados(
                todas_imagens, diretorio
            )
        elif opcao == 8:
            self._opcao_backup_manual(diretorio, todas_imagens)
        
        self.menu.imprimir_conclusao()
    
    def _opcao_duplicatas(self, imagens: List[ImageInfo], diretorio: str) -> None:
        """Executa detecção e remoção de duplicatas."""
        print("🔍 DETECTANDO E MOVENDO DUPLICATAS...")
        
        # Primeiro simula
        movidas = self.service.detect_and_move_duplicates(imagens, diretorio, simular=True)
        
        if movidas > 0 and self.menu.confirmar_operacao("Confirma mover duplicatas?"):
            self.service.detect_and_move_duplicates(imagens, diretorio, simular=False)
        elif movidas == 0:
            print("✅ Nenhuma duplicata encontrada!")
    
    def _opcao_renomear(self, imagens: List[ImageInfo], diretorio: str) -> None:
        """Executa renomeação de imagens."""
        print("📝 RENOMEANDO IMAGENS...")
        
        if not imagens:
            print("✅ Nenhuma imagem precisa ser renomeada!")
            return
        
        eventos = EventManager.solicitar_eventos()
        
        # Primeiro simula
        self.service.rename_images(imagens, diretorio, eventos, simular=True)
        
        if self.menu.confirmar_operacao("Confirma as alterações?"):
            self.service.rename_images(imagens, diretorio, eventos, simular=False)
            
            # Se foram adicionados eventos, oferece organização por pastas
            if eventos:
                self._oferecer_organizacao_pos_renomeacao(diretorio)
    
    def _opcao_processo_completo(
        self, 
        imagens_nao_org: List[ImageInfo], 
        imagens_org: List[ImageInfo],
        diretorio: str
    ) -> None:
        """Executa processo completo de organização."""
        print("🚀 EXECUTANDO PROCESSO COMPLETO...")
        
        # Primeiro mostra análise
        self.service.print_analysis_statistics(imagens_nao_org, imagens_org)
        
        todas_imagens = imagens_nao_org + imagens_org
        
        # Duplicatas
        duplicatas_movidas = self.service.detect_and_move_duplicates(
            todas_imagens, diretorio, simular=True
        )
        if duplicatas_movidas > 0 and self.menu.confirmar_operacao("Mover duplicatas?"):
            self.service.detect_and_move_duplicates(todas_imagens, diretorio, simular=False)
        
        # Renomeação
        if imagens_nao_org:
            eventos = EventManager.solicitar_eventos()
            self.service.rename_images(imagens_nao_org, diretorio, eventos, simular=True)
            
            if self.menu.confirmar_operacao("Confirma renomeação?"):
                self.service.rename_images(imagens_nao_org, diretorio, eventos, simular=False)
    
    def _opcao_relatorio(self, imagens: List[ImageInfo]) -> None:
        """Gera relatório detalhado."""
        print("📊 GERANDO RELATÓRIO DETALHADO...")
        self.service.generate_report(imagens)
    
    def _opcao_buscar_periodo(self, imagens: List[ImageInfo]) -> None:
        """Busca fotos por período."""
        print("🔍 BUSCAR FOTOS POR PERÍODO...")
        data_inicio, data_fim = self.menu.solicitar_periodo()
        
        fotos_periodo = self.service.search_photos_by_period(imagens, data_inicio, data_fim)
        
        if fotos_periodo:
            print(f"\n📋 ENCONTRADAS {len(fotos_periodo)} FOTOS NO PERÍODO:")
            print("─" * 50)
            for img in fotos_periodo:
                data = img.data_preferencial
                print(f"📷 {img.arquivo}")
                print(f"   📅 Data: {data.strftime('%d/%m/%Y %H:%M')}")
                print(f"   📏 Dimensões: {img.dimensoes}")
                print()
        else:
            print("❌ Nenhuma foto encontrada no período especificado.")
    
    def _opcao_organizar_eventos(self, imagens: List[ImageInfo], diretorio: str) -> None:
        """Organiza por pastas de eventos."""
        print("📁 ORGANIZANDO POR PASTAS DE EVENTOS...")
        
        # Primeiro simula
        movidos = self.service.organize_by_events(imagens, diretorio, simular=True)
        
        if movidos > 0 and self.menu.confirmar_operacao("Confirma a organização por pastas?"):
            self.service.organize_by_events(imagens, diretorio, simular=False)
        elif movidos == 0:
            print("📋 Nenhum evento detectado nos nomes dos arquivos.")
            print("💡 Dica: Adicione eventos aos nomes usando a opção de renomeação.")
    
    def _opcao_organizar_anos(self, imagens: List[ImageInfo], diretorio: str) -> None:
        """Organiza por anos usando sistema legado (compatibilidade)."""
        print("🎂 ORGANIZANDO POR ANOS (SISTEMA LEGADO)...")
        print("💡 Esta opção mantém compatibilidade com sistema anterior")
        
        # Primeiro simula
        anos_dict = self.service.organize_by_years(imagens, diretorio, simular=True)
        
        if anos_dict and self.menu.confirmar_operacao("Confirma a organização por anos?"):
            self.service.organize_by_years(imagens, diretorio, simular=False)
        elif not anos_dict:
            print("📅 Nenhuma imagem com data válida para organização por anos.")
            print("💡 As imagens devem ter datas a partir de 01/01/2025.")
    
    def _opcao_organizar_periodos_customizados(
        self, 
        imagens: List[ImageInfo], 
        diretorio: str
    ) -> None:
        """Organiza por períodos usando configuração personalizada."""
        print("📊 ORGANIZANDO POR PERÍODOS CUSTOMIZADOS...")
        
        if not self.configuration:
            print("⚠️  Configuração personalizada não foi definida!")
            print("💡 Use a opção 9 para configurar primeiro.")
            return
        
        # Mostra configuração
        print(f"📅 Período configurado: {self.configuration.data_inicio.strftime('%d/%m/%Y')}")
        if self.configuration.data_final:
            print(f"📅 Data final: {self.configuration.data_final.strftime('%d/%m/%Y')}")
        print(f"🏷️  Prefixo: {self.configuration.prefixo_nomenclatura}")
        
        # Primeiro simula
        print("\n🔍 Simulando organização...")
        resultado = self.service.organize_by_custom_periods(
            imagens, diretorio, self.configuration, simular=True)
        
        if not resultado:
            print("ℹ️  Nenhuma organização necessária.")
            return
        
        # Mostra resultado da simulação
        print("\n📊 Resultado da simulação:")
        for periodo, imgs in resultado.items():
            print(f"  📁 {periodo}: {len(imgs)} imagens")
        
        # Pergunta se executa
        if self.menu.confirmar_operacao("Executar organização por períodos?"):
            print("\n� Executando organização...")
            self.service.organize_by_custom_periods(
                imagens, diretorio, self.configuration, simular=False)
            print("✅ Organização concluída!")
    
    def _opcao_configuracao_personalizada(self) -> None:
        """Permite configurar parâmetros personalizados."""
        print("⚙️  CONFIGURAÇÃO PERSONALIZADA")
        print("=" * 50)
        
        opcoes = [
            "1️⃣  Configurar novo projeto personalizado",
            "2️⃣  Visualizar configuração atual"
        ]
        
        for opcao in opcoes:
            print(f"   {opcao}")
        
        escolha = input("\n🔢 Escolha uma opção (1-2): ").strip()
        
        if escolha == "1":
            self.configuration = ConfigurationManager.prompt_user_configuration()
            print("✅ Configuração personalizada aplicada!")
        elif escolha == "2":
            self._exibir_configuracao_atual()
        else:
            print("❌ Opção inválida!")
    
    def _exibir_configuracao_atual(self) -> None:
        """Exibe a configuração atual."""
        if not self.configuration:
            print("⚠️  Nenhuma configuração personalizada definida.")
            print("💡 Sistema está usando configuração padrão.")
            return
        
        print("\n📋 CONFIGURAÇÃO ATUAL:")
        print("=" * 40)
        print(f"📅 Data início: {self.configuration.data_inicio.strftime('%d/%m/%Y')}")
        if self.configuration.data_final:
            print(f"📅 Data final: {self.configuration.data_final.strftime('%d/%m/%Y')}")
        else:
            print("📅 Data final: Não definida")
        print(f"🏷️  Prefixo: {self.configuration.prefixo_nomenclatura}")
        print(f"📊 Período: {'Incluído' if self.configuration.incluir_periodo else 'Não incluído'}")
        print(f"🔢 Sequencial: {'Incluído' if self.configuration.incluir_sequencial else 'Não incluído'}")
        print(f"📝 Formato data: {self.configuration.formato_data}")
        print("=" * 40)
    
    def _opcao_backup_manual(self, diretorio: str, imagens: List[ImageInfo]) -> None:
        """Cria backup manual."""
        print("💾 CRIANDO BACKUP DO ESTADO ATUAL...")
        backup_file = self.service.create_manual_backup(diretorio)
        print("✅ Backup criado com sucesso!")
        print(f"📁 Arquivo: {backup_file}")
        print(f"📊 {len(imagens)} imagens registradas no backup.")
    
    def _oferecer_organizacao_pos_renomeacao(self, diretorio: str) -> None:
        """Oferece organização por pastas após renomeação com eventos."""
        print("\n🎉 EVENTOS DETECTADOS NA RENOMEAÇÃO!")
        print("💡 Quer organizar as fotos em pastas por evento?")
        
        if self.menu.confirmar_operacao("Organizar por pastas de eventos?"):
            # Recarrega as imagens para detectar os novos eventos
            imagens_atualizadas, _ = self.service.analyze_directory(diretorio)
            todas_atualizadas = imagens_atualizadas  # Só as não organizadas têm eventos
            
            movidos = self.service.organize_by_events(todas_atualizadas, diretorio, simular=True)
            if movidos > 0 and self.menu.confirmar_operacao("Confirma a organização?"):
                self.service.organize_by_events(todas_atualizadas, diretorio, simular=False)
