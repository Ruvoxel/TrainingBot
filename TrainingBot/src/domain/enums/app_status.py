from enum import StrEnum, auto
from typing import Final

class AppStatus(StrEnum):
    NO_DEFINED: Final[str] = auto()
    ERROR: Final[str] = auto()
    IN_PROGRESS: Final[str] = auto()
    START: Final[str] = auto()
    STOP: Final[str] = auto()
    BACK: Final[str] = auto()