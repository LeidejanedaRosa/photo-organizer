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


class PeriodCalculator:
    """Calcula períodos baseado em configuração personalizada."""
    
    def __init__(self, data_inicio: datetime):
        self.data_inicio = data_inicio
    
    def calculate_year(self, data: datetime) -> int:
        """
        Calcula qual ano do período baseado na data da foto.
        """
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
        """Calcula o mês do período baseado na data da foto."""
        if data < self.data_inicio:
            return 0
        
        # Calcula diferença em meses
        anos_diff = data.year - self.data_inicio.year
        meses_diff = anos_diff * 12 + (data.month - self.data_inicio.month)
        
        # Ajusta baseado no dia
        if data.day >= self.data_inicio.day:
            return meses_diff
        else:
            return meses_diff - 1 if meses_diff > 0 else 0


# Mantém compatibilidade com código existente
class BabyAge:
    """Compatibilidade com sistema anterior - calcula idade do bebê."""
    
    BIRTH_DATE = datetime(2024, 8, 17)
    
    @classmethod
    def calculate_year(cls, data: datetime) -> int:
        """Mantém compatibilidade - calcula ano do bebê."""
        calculator = PeriodCalculator(cls.BIRTH_DATE)
        return calculator.calculate_year(data)
    
    @classmethod
    def calculate_month(cls, data: datetime) -> int:
        """Mantém compatibilidade - calcula mês do bebê com lógica original."""
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
