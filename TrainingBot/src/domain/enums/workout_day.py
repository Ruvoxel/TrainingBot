from enum import StrEnum, auto
from typing import Final

class WorkoutDay(StrEnum):
    MONDAY: Final[str] = auto()
    TUESDAY: Final[str] = auto()
    WEDNESDAY: Final[str] = auto()
    THURSDAY: Final[str] = auto()
    FRIDAY: Final[str] = auto()
    SATURDAY: Final[str] = auto()
    SUNDAY: Final[str] = auto()