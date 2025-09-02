from typing import List

from ..domain.configuration import ConfigurationManager, ProjectConfiguration
from ..domain.image import ImageInfo, PeriodCalculator
from ..services.photo_organizer_service import PhotoOrganizerService
from ..utils.event_manager import EventManager
from .menu_controller import MenuController


class PhotoOrganizerCLI:

    def __init__(self):
        self.service = PhotoOrganizerService()
        self.menu = MenuController()
        self.configuration = None

    def run(self) -> None:
        try:
            directory = self.menu.request_directory()

            unorganized_images, organized_images = (
                self.service.analyze_directory(directory)
            )
            has_organized_photos = len(organized_images) > 0
            has_configuration = self.configuration is not None

            option = self.menu.display_smart_menu(
                has_organized_photos, has_configuration
            )

            self._execute_smart_option(
                option,
                directory,
                unorganized_images,
                organized_images,
                has_organized_photos,
                has_configuration,
            )
        except KeyboardInterrupt:
            print("\n\n👋 Programa encerrado pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("🔧 Verifique o diretório e tente novamente.")

    def _execute_smart_option(
        self,
        option: int,
        directory: str,
        unorganized_images: List[ImageInfo],
        organized_images: List[ImageInfo],
        has_organized_photos: bool,
        has_configuration: bool,
    ) -> None:
        self.menu.print_separator()

        if self.configuration:
            self.service.set_configuration(self.configuration)

        all_images = unorganized_images + organized_images

        if not has_organized_photos:
            if option == 1:
                self._option_custom_configuration()
            elif option == 2:
                self._option_duplicates(all_images, directory)
            elif option == 3:
                self._option_rename(unorganized_images, directory)
            elif option == 4:
                self._option_complete_process(
                    unorganized_images, organized_images, directory
                )
            elif option == 5:
                self._option_report(all_images)
        else:
            if option == 1:
                self._option_custom_configuration()
            elif option == 2:
                self._option_duplicates(all_images, directory)
            elif option == 3:
                self._option_rename(unorganized_images, directory)
            elif option == 4:
                self._option_complete_process(
                    unorganized_images, organized_images, directory
                )
            elif option == 5:
                self._option_organize_events(all_images, directory)
            elif option == 6:
                self._option_organize_custom_periods(all_images, directory)
            elif option == 7:
                self._option_search_period(all_images)
            elif option == 8:
                self._option_report(all_images)
            elif option == 9:
                self._option_manual_backup(directory, all_images)

        self.menu.print_conclusion()

    def _execute_legacy_option(self, option: int, directory: str) -> None:
        self.menu.print_separator()

        if option == 9:
            self._option_custom_configuration()
            return

        if self.configuration:
            self.service.set_configuration(self.configuration)

        unorganized_images, organized_images = self.service.analyze_directory(
            directory
        )
        all_images = unorganized_images + organized_images

        if option == 1:
            self._option_duplicates(all_images, directory)
        elif option == 2:
            self._option_rename(unorganized_images, directory)
        elif option == 3:
            self._option_complete_process(
                unorganized_images, organized_images, directory
            )
        elif option == 4:
            self._option_report(all_images)
        elif option == 5:
            self._option_search_period(all_images)
        elif option == 6:
            self._option_organize_events(all_images, directory)
        elif option == 7:
            self._option_organize_custom_periods(all_images, directory)
        elif option == 8:
            self._option_manual_backup(directory, all_images)

        self.menu.print_conclusion()

    def _guide_naming_configuration(self) -> None:
        print("\n" + "⚠️ " * 20)
        print("⚠️  CONFIGURAÇÃO DE NOMENCLATURA NECESSÁRIA")
        print("⚠️ " * 20)
        print()
        print("🔧 Para renomear fotos corretamente, você precisa primeiro")
        print("   configurar como deseja que suas fotos sejam nomeadas.")
        print()
        print("💡 OPÇÕES DISPONÍVEIS:")
        print("   📋 Opção 9️⃣  - Configure sua nomenclatura personalizada")
        print("   🎯 Depois volte e use a opção escolhida")
        print()
        print("🎨 EXEMPLO DE CONFIGURAÇÃO:")
        print("   📅 Data início: 01/01/2024")
        print("   🏷️  Prefixo: FOTO")
        print("   📊 Com numeração: 00-FOTO-01012024, 01-FOTO-02012024...")
        print("   📝 Sem numeração: FOTO-01012024, FOTO-02012024...")
        print()
        print("=" * 60)

        if self.menu.confirm_operation("Deseja configurar agora?"):
            self.configuration = (
                ConfigurationManager.prompt_user_configuration()
            )
            self.service.set_configuration(self.configuration)
            print(
                "✅ Configuração criada! Agora você pode usar as opções 2 e 3."
            )
        else:
            print("👋 Use a opção 9 quando estiver pronto para configurar.")

    def _option_duplicates(
        self, images: List[ImageInfo], directory: str
    ) -> None:
        print("🔍 DETECTANDO E MOVENDO DUPLICATAS...")

        moved = self.service.detect_and_move_duplicates(
            images, directory, simular=True
        )

        if moved > 0 and self.menu.confirm_operation(
            "Confirma mover duplicatas?"
        ):
            self.service.detect_and_move_duplicates(
                images, directory, simular=False
            )
        elif moved == 0:
            print("✅ Nenhuma duplicate encontrada!")

    def _option_rename(self, images: List[ImageInfo], directory: str) -> None:
        print("📝 RENOMEANDO IMAGENS...")

        if not images:
            print("✅ Nenhuma imagem precisa ser renomeada!")
            return

        if not self.configuration:
            self._guide_naming_configuration()
            return

        events = {}
        if self.menu.confirm_operation(
            "Deseja configurar events especiais para as fotos?"
        ):
            events = EventManager.request_events()

        self.service.rename_images(images, directory, events, simular=True)

        if self.menu.confirm_operation("Confirma as alterações?"):
            self.service.rename_images(
                images, directory, events, simular=False
            )

            if events:
                self._offer_post_rename_organization(directory)

    def _option_complete_process(
        self,
        unorganized_images: List[ImageInfo],
        organized_images: List[ImageInfo],
        directory: str,
    ) -> None:

        print("🚀 EXECUTANDO PROCESSO COMPLETO...")

        self.service.print_analysis_statistics(
            unorganized_images, organized_images
        )

        all_images = unorganized_images + organized_images

        moved_duplicates = self.service.detect_and_move_duplicates(
            all_images, directory, simular=True
        )
        if moved_duplicates > 0 and self.menu.confirm_operation(
            "Mover duplicatas?"
        ):
            self.service.detect_and_move_duplicates(
                all_images, directory, simular=False
            )

        if unorganized_images:
            if not self.configuration:
                self._guide_naming_configuration()
                return

            events = {}
            if self.menu.confirm_operation(
                "Deseja configurar events especiais para as fotos?"
            ):
                events = EventManager.request_events()

            self.service.rename_images(
                unorganized_images, directory, events, simular=True
            )

            if self.menu.confirm_operation("Confirma renomeação?"):
                self.service.rename_images(
                    unorganized_images, directory, events, simular=False
                )

    def _option_report(self, images: List[ImageInfo]) -> None:

        print("📊 GERANDO RELATÓRIO DETALHADO...")
        self.service.generate_report(images)

    def _option_search_period(self, images: List[ImageInfo]) -> None:

        print("🔍 BUSCAR FOTOS POR PERÍODO...")
        start_date, end_date = self.menu.request_period()

        period_photos = self.service.search_photos_by_period(
            images, start_date, end_date
        )

        if period_photos:
            print(f"\n📋 ENCONTRADAS {len(period_photos)} FOTOS NO PERÍODO:")
            print("─" * 50)
            for img in period_photos:
                date = img.preferred_date
                print(f"📷 {img.file}")
                print(f"   📅 Data: {date.strftime('%d/%m/%Y %H:%M')}")
                print(f"   📏 Dimensões: {img.dimensions}")
                print()
        else:
            print("❌ Nenhuma foto encontrada no período especificado.")

    def _option_organize_events(
        self, images: List[ImageInfo], directory: str
    ) -> None:

        print("📁 ORGANIZANDO POR PASTAS DE EVENTOS...")

        moved = self.service.organize_by_events(
            images, directory, simular=True
        )

        if moved > 0 and self.menu.confirm_operation(
            "Confirma a organização por pastas?"
        ):
            self.service.organize_by_events(images, directory, simular=False)
        elif moved == 0:
            print("📋 Nenhum evento detectado nos nomes dos arquivos.")
            print(
                "💡 Dica: Adicione events aos nomes usando a opção de renomeação."
            )

    def _option_organize_years(
        self, images: List[ImageInfo], directory: str
    ) -> None:

        print("🎂 ORGANIZANDO POR ANOS (SISTEMA LEGADO)...")
        print("💡 Esta opção mantém compatibilidade com sistema anterior")

        years_dict = self.service.organize_by_years(
            images, directory, simular=True
        )

        if years_dict and self.menu.confirm_operation(
            "Confirma a organização por anos?"
        ):
            self.service.organize_by_years(images, directory, simular=False)
        elif not years_dict:
            print(
                "📅 Nenhuma imagem com date válida para organização por anos."
            )
            print("💡 As images devem ter datas a partir de 01/01/2025.")

    def _option_organize_custom_periods(
        self, images: List[ImageInfo], directory: str
    ) -> None:

        print("📊 ORGANIZANDO POR PERÍODOS CUSTOMIZADOS...")

        if not self.configuration:
            print("⚠️  Configuração personalizada não foi definida!")
            print("💡 Use a opção 9 para configurar primeiro.")
            return

        print(
            f"📅 Período configurado: {self.configuration.start_date.strftime('%d/%m/%Y')}"
        )
        if self.configuration.end_date:
            print(
                f"📅 Data final: {self.configuration.end_date.strftime('%d/%m/%Y')}"
            )
        print(f"🏷️  Prefixo: {self.configuration.naming_prefix}")

        print("\n🔍 Simulando organização...")
        result = self.service.organize_by_custom_periods(
            images, directory, self.configuration, simular=True
        )

        if not result:
            print("ℹ️  Nenhuma organização necessária.")
            return

        print("\n📊 Resultado da simulação:")
        for period, imgs in result.items():
            print(f"  📁 {period}: {len(imgs)} images")

        if self.menu.confirm_operation("Executar organização por períodos?"):
            print("\n� Executando organização...")
            self.service.organize_by_custom_periods(
                images, directory, self.configuration, simular=False
            )
            print("✅ Organização concluída!")

    def _option_custom_configuration(self) -> None:

        print("⚙️  CONFIGURAÇÃO PERSONALIZADA")
        print("=" * 50)

        opcoes = [
            "1️⃣  Configurar novo projeto personalizado",
            "2️⃣  Visualizar configuração atual",
        ]

        for option in opcoes:
            print(f"   {option}")

        choice = input("\n🔢 Escolha uma opção (1-2): ").strip()

        if choice == "1":
            self.configuration = (
                ConfigurationManager.prompt_user_configuration()
            )
            self.service.set_configuration(self.configuration)
            print("✅ Configuração personalizada aplicada!")
        elif choice == "2":
            self._display_current_configuration()
        else:
            print("❌ Opção inválida!")

    def _display_current_configuration(self) -> None:

        if not self.configuration:
            print("⚠️  Nenhuma configuração personalizada definida.")
            print("💡 Sistema está usando configuração padrão.")
            return

        print("\n📋 CONFIGURAÇÃO ATUAL:")
        print("=" * 40)
        print(
            f"📅 Data início: {self.configuration.start_date.strftime('%d/%m/%Y')}"
        )
        if self.configuration.end_date:
            print(
                f"📅 Data final: {self.configuration.end_date.strftime('%d/%m/%Y')}"
            )
        else:
            print("📅 Data final: Não definida")
        print(f"🏷️  Prefixo: {self.configuration.naming_prefix}")
        print(
            f"📊 Período: {'Incluído' if self.configuration.include_period else 'Não incluído'}"
        )
        print(
            f"🔢 Sequencial: {'Incluído' if self.configuration.include_sequential else 'Não incluído'}"
        )
        print(f"📝 Formato date: {self.configuration.date_format}")
        print("=" * 40)

    def _option_manual_backup(
        self, directory: str, images: List[ImageInfo]
    ) -> None:

        print("💾 CRIANDO BACKUP DO ESTADO ATUAL...")
        backup_file = self.service.create_manual_backup(directory)
        print("✅ Backup criado com sucesso!")
        print(f"📁 Arquivo: {backup_file}")
        print(f"📊 {len(images)} images registradas no backup.")

    def _offer_post_rename_organization(self, directory: str) -> None:

        print("\n🎉 EVENTOS DETECTADOS NA RENOMEAÇÃO!")
        print("💡 Quer organizar as fotos em pastas por evento?")

        if self.menu.confirm_operation("Organizar por pastas de events?"):
            updated_images, _ = self.service.analyze_directory(directory)
            all_updated = updated_images

            moved = self.service.organize_by_events(
                all_updated, directory, simular=True
            )
            if moved > 0 and self.menu.confirm_operation(
                "Confirma a organização?"
            ):
                self.service.organize_by_events(
                    all_updated, directory, simular=False
                )
