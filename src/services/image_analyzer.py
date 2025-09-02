import os
import hashlib
from datetime import datetime
from typing import List, Optional
from PIL import Image
from PIL.ExifTags import TAGS

from ..domain.image import ImageInfo

class ImageAnalyzer:
    
    def analyze_image(self, caminho: str) -> Optional[ImageInfo]:
        
        try:
            with Image.open(caminho) as img:
                data_mod = datetime.fromtimestamp(os.path.getmtime(caminho))
                fmt = img.format or "Desconhecido"
                hash_imagem = self._calculate_image_hash(caminho)
                
                return ImageInfo(
                    arquivo=os.path.basename(caminho),
                    formato=fmt,
                    dimensoes=img.size,
                    modo=img.mode,
                    tamanho=os.path.getsize(caminho),
                    data_mod=data_mod,
                    data_exif=self._extract_exif_date(img),
                    hash_imagem=hash_imagem
                )
        except (IOError, OSError) as e:
            print(f"Não foi possível ler '{os.path.basename(caminho)}': {e}")
            return None
    
    def _extract_exif_date(self, img: Image.Image) -> Optional[datetime]:
        
        try:
            exif = img.getexif()
            if exif is not None:
                for tag_id in exif:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exif.get(tag_id)
                    if tag == 'DateTimeOriginal':
                        return datetime.strptime(data, '%Y:%m:%d %H:%M:%S')
        except (AttributeError, ValueError, TypeError):
            return None
        return None
    
    def _calculate_image_hash(self, caminho: str) -> str:
        
        hasher = hashlib.md5()
        try:
            with Image.open(caminho) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img_bytes = img.tobytes()
                hasher.update(img_bytes)
        except (IOError, OSError) as e:
            print(f"Erro ao calcular hash de {caminho}: {e}")
            return ""
        return hasher.hexdigest()
    
    def analyze_directory(self, diretorio: str) -> List[ImageInfo]:
        
        imagens = []
        
        for arquivo in os.listdir(diretorio):
            caminho = os.path.join(diretorio, arquivo)
            if os.path.isfile(caminho):
                info = self.analyze_image(caminho)
                if info:
                    imagens.append(info)
        
        return imagens