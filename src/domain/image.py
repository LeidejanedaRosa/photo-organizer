from datetime import datetime
from pathlib import Path
from typing import Optional


class ImageInfo:

    def __init__(
        self,
        file: str,
        format: Optional[str],
        dimensions: tuple,
        mode: str,
        size: int,
        data_mod: datetime,
        data_exif: Optional[datetime] = None,
        hash_image: Optional[str] = None,
    ):
        self.file = file
        self.format = format
        self.dimensions = dimensions
        self.mode = mode
        self.size = size
        self.data_mod = data_mod
        self.data_exif = data_exif
        self.hash_image = hash_image

    @property
    def preferred_date(self) -> datetime:

        return self.data_exif or self.data_mod

    @property
    def extension(self) -> str:

        return Path(self.file).suffix

    @property
    def name_without_extension(self) -> str:

        return Path(self.file).stem

    def __eq__(self, other):

        if not isinstance(other, ImageInfo):
            return False
        return (
            self.hash_image == other.hash_image and self.hash_image is not None
        )

    def __hash__(self):

        return hash(self.file)


class PeriodCalculator:

    def __init__(self, start_date: datetime):
        self.start_date = start_date

    def calculate_year(self, date: datetime) -> int:

        if date < self.start_date:
            return 0

        years_gone_by = date.year - self.start_date.year
        current_birthday = datetime(
            date.year, self.start_date.month, self.start_date.day
        )

        if date >= current_birthday:
            return years_gone_by + 1
        else:
            return years_gone_by if years_gone_by > 0 else 1

    def calculate_month(self, date: datetime) -> int:

        if date < self.start_date:
            return 0

        years_diff = date.year - self.start_date.year
        months_diff = years_diff * 12 + (date.month - self.start_date.month)

        if date.day >= self.start_date.day:
            return months_diff
        else:
            return months_diff - 1 if months_diff > 0 else 0


class Event:

    def __init__(self, date: str, description: str):
        self.date = date
        self.description = description

    def __str__(self):
        return self.description
