import hashlib
import os
from datetime import datetime
from typing import List, Optional

from PIL import ExifTags, Image

from src.domain.image import ImageInfo


class ImageAnalyzer:

    def analyze_image(self, path: str) -> Optional[ImageInfo]:

        try:
            with Image.open(path) as img:
                data_mod = datetime.fromtimestamp(os.path.getmtime(path))
                fmt = img.format or "Desconhecido"
                hash_image = self._calculate_image_hash(path)

                return ImageInfo(
                    file=os.path.basename(path),
                    format=fmt,
                    dimensions=img.size,
                    mode=img.mode,
                    size=os.path.getsize(path),
                    data_mod=data_mod,
                    data_exif=self._extract_exif_date(img),
                    hash_image=hash_image,
                )
        except (IOError, OSError) as e:
            print(f"Não foi possível ler '{os.path.basename(path)}': {e}")
            return None

    def _extract_exif_date(self, img: Image.Image) -> Optional[datetime]:

        try:
            exif = img.getexif()
            if exif is not None:
                for tag_id in exif:
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    date = exif.get(tag_id)
                    if tag == "DateTimeOriginal" and date:
                        return datetime.strptime(
                            str(date), "%Y:%m:%d %H:%M:%S"
                        )
        except (AttributeError, ValueError, TypeError):
            return None
        return None

    def _calculate_image_hash(self, path: str) -> str:

        hasher = hashlib.md5()
        try:
            with Image.open(path) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img_bytes = img.tobytes()
                hasher.update(img_bytes)
        except (IOError, OSError) as e:
            print(f"Erro ao calcular hash de {path}: {e}")
            return ""
        return hasher.hexdigest()

    def analyze_directory(self, directory: str) -> List[ImageInfo]:

        images = []

        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if os.path.isfile(path):
                info = self.analyze_image(path)
                if info:
                    images.append(info)

        return images
