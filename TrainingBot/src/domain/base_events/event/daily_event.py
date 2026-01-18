from pydantic import BaseModel, PositiveFloat, field_validator
from pydantic.config import ConfigDict
from typing import Optional, Final

from ...user import UserID
from ...errors import TotalCaloriesError

class DayliEvent(BaseModel):
    Id: Final[UserID]
    TotalCalories: PositiveFloat

    model_config: ConfigDict = ConfigDict(frozen=True)


    @field_validator("TotalCalories", mode="before")
    def TotalCalories_validator(cls: DayliEvent, value: float) -> Optional[float]:
        if value <= 0:
            raise TotalCaloriesError()
        return value