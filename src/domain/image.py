import os
from datetime import datetime
from pathlib import Path
from typing import Optional

class ImageInfo:
    
    def __init__(
        self,
        arquivo: str,
        formato: Optional[str],
        dimensoes: tuple,
        modo: str,
        tamanho: int,
        data_mod: datetime,
        data_exif: Optional[datetime] = None,
        hash_imagem: Optional[str] = None
    ):
        self.arquivo = arquivo
        self.formato = formato
        self.dimensoes = dimensoes
        self.modo = modo
        self.tamanho = tamanho
        self.data_mod = data_mod
        self.data_exif = data_exif
        self.hash_imagem = hash_imagem
    
    @property
    def data_preferencial(self) -> datetime:
        
        return self.data_exif or self.data_mod
    
    @property
    def extensao(self) -> str:
        
        return Path(self.arquivo).suffix
    
    @property
    def nome_sem_extensao(self) -> str:
        
        return Path(self.arquivo).stem
    
    def __eq__(self, other):
        
        if not isinstance(other, ImageInfo):
            return False
        return self.hash_imagem == other.hash_imagem and self.hash_imagem is not None
    
    def __hash__(self):
        
        return hash(self.arquivo)

class PeriodCalculator:
    
    def __init__(self, data_inicio: datetime):
        self.data_inicio = data_inicio
    
    def calculate_year(self, data: datetime) -> int:
        
        if data < self.data_inicio:
            return 0
        
        anos_passados = data.year - self.data_inicio.year
        aniversario_atual = datetime(
            data.year,
            self.data_inicio.month,
            self.data_inicio.day
        )
        
        if data >= aniversario_atual:
            return anos_passados + 1
        else:
            return anos_passados if anos_passados > 0 else 1
    
    def calculate_month(self, data: datetime) -> int:
        
        if data < self.data_inicio:
            return 0
        
        anos_diff = data.year - self.data_inicio.year
        meses_diff = anos_diff * 12 + (data.month - self.data_inicio.month)
        
        if data.day >= self.data_inicio.day:
            return meses_diff
        else:
            return meses_diff - 1 if meses_diff > 0 else 0

class Event:
    
    def __init__(self, data: str, descricao: str):
        self.data = data  
        self.descricao = descricao
    
    def __str__(self):
        return self.descricao