from enum import StrEnum, auto
from typing import Final

class WorkoutType(StrEnum):
    FITNES: Final[str] = auto()
    POWER: Final[str] = auto()
    WEIGHT_LOSS: Final[str] = auto() 