import os
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

from ..domain.configuration import ProjectConfiguration
from ..domain.image import ImageInfo
from ..utils.base_organizer import BaseOrganizer
from ..utils.file_manager import FileManager
from ..utils.ui_formatter import UIFormatter


class YearOrganizer(BaseOrganizer):

    def _group_images(
        self, images: List[ImageInfo]
    ) -> Dict[str, List[ImageInfo]]:

        imagens_por_ano = defaultdict(list)

        for img in images:
            date = img.preferred_date
            ano = date.year
            imagens_por_ano[f"Ano {ano}"].append(img)

        return dict(imagens_por_ano)

    def _get_operation_name(self) -> str:
        return "Organizando por anos"

    def _get_empty_message(self) -> str:
        return "Nenhuma imagem com data válida para organização por anos."


class EventOrganizer:

    def __init__(self):
        self.ui_formatter = UIFormatter()
        self.file_manager = FileManager()

    def organize_by_events(
        self,
        directory: str,
        eventos_detectados: Dict[str, List[str]],
        simular: bool = True,
    ) -> int:

        if not eventos_detectados:
            print("📋 Nenhum evento detectado nos nomes dos arquivos.")
            return 0

        self.ui_formatter.print_operation_header(
            "Organizando por eventos", simular
        )
        self.ui_formatter.print_separator()

        total_moved = 0

        for evento, arquivos in eventos_detectados.items():
            pasta_evento = os.path.join(directory, evento)

            self.ui_formatter.print_group_header(
                evento, len(arquivos), "arquivo(s)"
            )

            if not simular:
                self.file_manager.create_directory_if_not_exists(
                    pasta_evento, evento
                )
            else:
                print(f"   📁 Criaria pasta: {evento}/")

            for arquivo in arquivos:
                origem = os.path.join(directory, arquivo)
                destino = os.path.join(pasta_evento, arquivo)

                if self.file_manager.move_single_file(
                    origem, destino, arquivo, simular
                ):
                    if not simular:
                        total_moved += 1
                else:
                    total_moved += 1 if simular else 0

        self.ui_formatter.print_operation_result(
            "Organização por eventos", total_moved, "arquivos", simular
        )

        return total_moved


class FolderOrganizer:

    def __init__(self):
        self.year_organizer = YearOrganizer()
        self.event_organizer = EventOrganizer()
        self.ui_formatter = UIFormatter()
        self.file_manager = FileManager()

    def organize_by_years(
        self, images: List[ImageInfo], directory: str, simular: bool = True
    ) -> Dict[int, List[ImageInfo]]:

        result = self.year_organizer.organize(images, directory, simular)

        converted_result = {}
        for key, value in result.items():
            year = int(key.replace("Ano ", ""))
            converted_result[year] = value

        return converted_result

    def organize_by_events(
        self,
        directory: str,
        eventos_detectados: Dict[str, List[str]],
        simular: bool = True,
    ) -> int:

        return self.event_organizer.organize_by_events(
            directory, eventos_detectados, simular
        )

    def detect_events_in_files(
        self, images: List[ImageInfo]
    ) -> Dict[str, List[str]]:

        eventos = defaultdict(list)

        for img in images:
            filename = Path(img.file).stem

            if " - " in filename:
                parts = filename.split(" - ")
                if len(parts) >= 2:
                    event_part = " - ".join(parts[1:])
                    if event_part and not event_part.isdigit():
                        eventos[event_part].append(img.file)

        return dict(eventos)

    def organize_by_custom_periods(
        self,
        images: List[ImageInfo],
        directory: str,
        configuration: ProjectConfiguration,
        simular: bool = True,
    ) -> Dict[str, List[ImageInfo]]:

        if not self.ui_formatter.validate_list_not_empty(
            images, "Nenhuma imagem para organizar por períodos."
        ):
            return {}

        imagens_periodo_atual = []
        imagens_periodo_futuro = []

        for img in images:
            period_number = configuration.calculate_period_number(
                img.preferred_date
            )
            if period_number == configuration.calculate_period_number(
                configuration.start_date
            ):
                imagens_periodo_atual.append(img)
            else:
                imagens_periodo_futuro.append(img)

        self.ui_formatter.print_operation_header(
            "Organizando por períodos customizados", simular
        )
        self.ui_formatter.print_separator()

        result = {}

        if imagens_periodo_atual:
            nome_pasta_atual = self._gerar_nome_pasta_periodo(configuration)
            result[nome_pasta_atual] = imagens_periodo_atual

            if not simular:
                self._criar_pasta_e_mover(
                    imagens_periodo_atual, directory, nome_pasta_atual
                )

            print(
                f"📁 {nome_pasta_atual}: {len(imagens_periodo_atual)} imagens"
            )

        if imagens_periodo_futuro:
            nova_config = configuration.create_next_period()
            if nova_config:
                nome_pasta_futura = self._gerar_nome_pasta_periodo(nova_config)
                result[nome_pasta_futura] = imagens_periodo_futuro

                if not simular:
                    self._criar_pasta_e_mover(
                        imagens_periodo_futuro, directory, nome_pasta_futura
                    )

                print(
                    f"📁 {nome_pasta_futura}: {len(imagens_periodo_futuro)} imagens"
                )

        self.ui_formatter.print_separator()
        return result

    def _gerar_nome_pasta_periodo(self, config: ProjectConfiguration) -> str:

        components = []

        if config.include_period:
            period_num = config.calculate_period_number(config.start_date)
            components.append(f"{period_num:02d}")

        components.append(config.naming_prefix)

        date_str = config.start_date.strftime(config.date_format)
        components.append(date_str)

        nome = config.separador.join(components)

        return nome

    def _criar_pasta_e_mover(
        self, images: List[ImageInfo], diretorio_base: str, folder_name: str
    ) -> None:

        pasta_destino = os.path.join(diretorio_base, folder_name)

        self.file_manager.create_directory_if_not_exists(
            pasta_destino, folder_name
        )

        for img in images:
            origem = os.path.join(diretorio_base, img.file)
            destino = os.path.join(pasta_destino, img.file)

            try:
                shutil.move(origem, destino)
                img.file = os.path.join(
                    folder_name, os.path.basename(img.file)
                )
                print(f"   📤 Movida: {img.file}")
            except (IOError, OSError) as e:
                print(f"   ❌ Erro ao mover {img.file}: {e}")
