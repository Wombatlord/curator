from enum import Enum
import typing
from src.adaptors.source import Result
from src.adaptors.harvard_art_museum import Source as _HAM_Source

class Museum(Enum):
    HAM = "harvard_art_museum"

    def get_source(self) -> typing.Sequence[Result]:
        match self:
            case Museum.HAM:
                return _HAM_Source