import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class ImageInfo:

    def __init__(
        self,
        file: str,
        formato: Optional[str],
        dimensions: tuple,
        modo: str,
        tamanho: int,
        data_mod: datetime,
        data_exif: Optional[datetime] = None,
        hash_imagem: Optional[str] = None,
    ):
        self.file = file
        self.formato = formato
        self.dimensions = dimensions
        self.modo = modo
        self.tamanho = tamanho
        self.data_mod = data_mod
        self.data_exif = data_exif
        self.hash_imagem = hash_imagem

    @property
    def preferred_date(self) -> datetime:

        return self.data_exif or self.data_mod

    @property
    def extension(self) -> str:

        return Path(self.file).suffix

    @property
    def nome_sem_extensao(self) -> str:

        return Path(self.file).stem

    def __eq__(self, other):

        if not isinstance(other, ImageInfo):
            return False
        return (
            self.hash_imagem == other.hash_imagem
            and self.hash_imagem is not None
        )

    def __hash__(self):

        return hash(self.file)


class PeriodCalculator:

    def __init__(self, start_date: datetime):
        self.start_date = start_date

    def calculate_year(self, date: datetime) -> int:

        if date < self.start_date:
            return 0

        anos_passados = date.year - self.start_date.year
        aniversario_atual = datetime(
            date.year, self.start_date.month, self.start_date.day
        )

        if date >= aniversario_atual:
            return anos_passados + 1
        else:
            return anos_passados if anos_passados > 0 else 1

    def calculate_month(self, date: datetime) -> int:

        if date < self.start_date:
            return 0

        anos_diff = date.year - self.start_date.year
        meses_diff = anos_diff * 12 + (date.month - self.start_date.month)

        if date.day >= self.start_date.day:
            return meses_diff
        else:
            return meses_diff - 1 if meses_diff > 0 else 0


class Event:

    def __init__(self, date: str, description: str):
        self.date = date
        self.description = description

    def __str__(self):
        return self.description
