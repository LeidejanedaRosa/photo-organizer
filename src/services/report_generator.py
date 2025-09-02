from collections import defaultdict
from datetime import datetime
from typing import List

from ..domain.image import ImageInfo


class ReportGenerator:

    def generate_detailed_report(self, images: List[ImageInfo]) -> None:

        if not images:
            print("📋 Nenhuma imagem para analisar no relatório.")
            return

        print("\n" + "=" * 70)
        print("📊 RELATÓRIO DETALHADO DAS IMAGENS")
        print("=" * 70)

        total_images = len(images)
        total_size = sum(img.size for img in images)

        self._analyze_formats(images, total_images)
        self._analyze_dimensions(images, total_images)
        self._analyze_temporal_data(images, total_images, total_size)

        print("=" * 70)

    def _analyze_formats(self, images: List[ImageInfo], total: int) -> None:

        formats = defaultdict(int)
        sizes_per_format = defaultdict(int)

        for img in images:
            formats[img.format] += 1
            sizes_per_format[img.format] += img.size

        print("\n🎨 DISTRIBUIÇÃO POR FORMATO:")
        for format, count in sorted(formats.items()):
            size_mb = sizes_per_format[format] / (1024 * 1024)
            percentage = (count / total) * 100
            print(
                f"   📄 {format}: {count} arquivos ({percentage:.1f}%) - "
                f"{size_mb:.2f} MB"
            )

    def _analyze_dimensions(self, images: List[ImageInfo], total: int) -> None:

        dimensions = defaultdict(int)

        for img in images:
            dim_str = f"{img.dimensions[0]}x{img.dimensions[1]}"
            dimensions[dim_str] += 1

        print("\n📐 RESOLUÇÕES MAIS COMUNS:")
        top_dimensions = sorted(
            dimensions.items(), key=lambda x: x[1], reverse=True
        )[:5]
        for dim, count in top_dimensions:
            percentage = (count / total) * 100
            print(f"   🖼️  {dim}: {count} images ({percentage:.1f}%)")

    def _analyze_temporal_data(
        self, images: List[ImageInfo], total: int, total_size: int
    ) -> None:

        print("\n📈 ESTATÍSTICAS GERAIS:")
        print(f"   📷 Total de images: {total}")
        print(f"   💾 Tamanho total: {total_size / (1024*1024):.2f} MB")
        print(f"   📏 Tamanho médio: {total_size / total / 1024:.1f} KB")

        if images:
            dates = [img.preferred_date for img in images]
            oldest_date = min(dates)
            newest_date = max(dates)
            period = (newest_date - oldest_date).days

            print("\n⏰ ANÁLISE TEMPORAL:")
            print(
                f"   📆 Foto mais antiga: "
                f"{oldest_date.strftime('%d/%m/%Y %H:%M')}"
            )
            print(
                f"   📆 Foto mais recente: "
                f"{newest_date.strftime('%d/%m/%Y %H:%M')}"
            )
            print(f"   📊 Período abrangido: {period} dias")

            if period > 0:
                frequency = total / period
                print(f"   📈 Frequência média: {frequency:.2f} fotos/dia")

    def search_photos_by_period(
        self, images: List[ImageInfo], start_date: str, end_date: str
    ) -> List[ImageInfo]:

        try:
            start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
            end_date_obj = datetime.strptime(end_date, "%d/%m/%Y")
            end_date_obj = end_date_obj.replace(hour=23, minute=59, second=59)

            period_photos = []
            for img in images:
                photo_date = img.preferred_date
                if start_date_obj <= photo_date <= end_date_obj:
                    period_photos.append(img)

            return period_photos
        except ValueError:
            print("❌ Formato de data inválido! Use DD/MM/AAAA")
            return []
