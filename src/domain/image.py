import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class ImageInfo:
    """Representa as informações de uma imagem."""
    
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
        """Retorna a data EXIF se disponível, senão a data de modificação."""
        return self.data_exif or self.data_mod
    
    @property
    def extensao(self) -> str:
        """Retorna a extensão do arquivo."""
        return Path(self.arquivo).suffix
    
    @property
    def nome_sem_extensao(self) -> str:
        """Retorna o nome do arquivo sem extensão."""
        return Path(self.arquivo).stem
    
    def __eq__(self, other):
        """Compara duas imagens baseado em seus hashes."""
        if not isinstance(other, ImageInfo):
            return False
        return self.hash_imagem == other.hash_imagem and self.hash_imagem is not None
    
    def __hash__(self):
        """Retorna o hash do objeto para uso em coleções."""
        return hash(self.arquivo)


class BabyAge:
    """Representa a idade do bebê e operações relacionadas."""
    
    BIRTH_DATE = datetime(2024, 8, 17)
    
    @classmethod
    def calculate_year(cls, data: datetime) -> int:
        """
        Calcula qual ano do bebê baseado na data da foto.
        Ano 1: 17/08/2024 a 16/08/2025
        Ano 2: 17/08/2025 a 16/08/2026
        """
        if data < cls.BIRTH_DATE:
            return 0
        
        anos_passados = data.year - cls.BIRTH_DATE.year
        aniversario_atual = datetime(data.year, 8, 17)
        
        if data >= aniversario_atual:
            return anos_passados + 1
        else:
            return anos_passados
    
    @classmethod
    def calculate_month(cls, data: datetime) -> int:
        """Calcula o mês do bebê baseado na data da foto."""
        mes = data.month
        dia = data.day
        
        if mes == 8:
            if dia >= 17:
                return 0  # Mês 00
            else:
                return 12  # Mês 12
        
        if mes >= 9:  # Setembro a dezembro
            return mes - 8
        else:  # Janeiro a julho
            return mes + 4


class Event:
    """Representa um evento associado a uma data."""
    
    def __init__(self, data: str, descricao: str):
        self.data = data  # Formato DDMMAAAA
        self.descricao = descricao
    
    def __str__(self):
        return self.descricao
