from enum import Enum

from src.adaptors.source import Result, Source
from src.adaptors.harvard_art_museum import Source as _HAM_Source

class Museum(Enum):
    HAM = "harvard_art_museum"

    def get_source(self) -> type[Source]:
        match self:
            case Museum.HAM:
                return _HAM_Source