import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional

from ..domain.configuration import ConfigurationManager, ProjectConfiguration
from ..domain.image import ImageInfo
from ..utils.ui_formatter import UIFormatter


class FilenameGenerator:

    def __init__(self, configuration: Optional[ProjectConfiguration] = None):

        if configuration is None:
            from datetime import datetime

            configuration = ConfigurationManager.create_custom_configuration(
                start_date=datetime.now().replace(month=1, day=1),
                prefix="IMG",
                include_period=True,
            )
        self.configuration = configuration

    def generate_filename(
        self,
        info: ImageInfo,
        sequential_number: int = 0,
        events: Optional[Dict[str, str]] = None,
    ) -> str:

        date = info.preferred_date

        if not self.configuration.is_date_in_range(date):

            base_name = date.strftime(self.configuration.date_format)
            if self.configuration.include_sequential:
                base_name += f"({sequential_number:02d})"
        else:

            event_str = None
            if events:
                date_fmt = date.strftime("%d%m%Y")
                event_str = events.get(date_fmt)

            base_name = self.configuration.generate_filename_pattern(
                date, sequential_number, event_str
            )

        return base_name + info.extension

    def is_organized(self, filename: str) -> bool:

        filename_without_ext = Path(filename).stem

        old_pattern = r"^\d{2} - IMG \d{8}\(\d{2}\)(?:\s-\s.+)?$"

        new_pattern = r".*\d{8}\(\d{2}\)(?:\s-\s.+)?$"

        return bool(re.match(old_pattern, filename_without_ext)) or bool(
            re.match(new_pattern, filename_without_ext)
        )


class FileRenamer:

    def __init__(self):
        self.filename_generator = FilenameGenerator()
        self.ui_formatter = UIFormatter()

    def rename_images(
        self,
        images: List[ImageInfo],
        directory: str,
        events: Optional[Dict[str, str]] = None,
        simulate: bool = True,
    ) -> int:

        if simulate:
            print("\n🔄 SIMULAÇÃO: Renomeando arquivos...")
        else:
            print("\n✨ RENOMEANDO ARQUIVOS...")

        print("─" * 60)

        groups = self._group_by_date(images)
        total_renamed = 0
        total_errors = 0

        for _, daily_images in groups.items():
            daily_images.sort(key=lambda x: x.preferred_date)

            for idx, img in enumerate(daily_images):
                current_path = os.path.join(directory, img.file)
                new_name = self.filename_generator.generate_filename(
                    img, sequential_number=idx, events=events
                )
                new_path = os.path.join(directory, new_name)

                if simulate:
                    print(f"📄 {img.file}")
                    print(f"   ➡️  {new_name}")
                else:
                    print(f"📄 Renomeando: {img.file}")
                    try:
                        shutil.move(current_path, new_path)
                        total_renamed += 1
                        print(f"   ✅ Sucesso: {new_name}")
                    except (IOError, OSError) as e:
                        total_errors += 1
                        print(f"   ❌ Erro: {e}")

        if not simulate:
            print("─" * 60)
            print("📊 RESULTADO:")
            print(f"   ✅ Renomeados com sucesso: {total_renamed}")
            print(f"   ❌ Erros: {total_errors}")
            print("─" * 60)

        return total_renamed

    def _group_by_date(
        self, images: List[ImageInfo]
    ) -> Dict[str, List[ImageInfo]]:

        groups: Dict[str, List[ImageInfo]] = {}
        for img in images:
            date = img.preferred_date.strftime("%d%m%Y")
            if date not in groups:
                groups[date] = []
            groups[date].append(img)
        return groups
