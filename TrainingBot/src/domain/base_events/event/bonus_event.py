from pydantic import BaseModel, PositiveFloat, field_validator
from pydantic.config import ConfigDict
from typing import Final, Optional

from ...user import UserID
from ...errors import AmountError

class BonusEvent(BaseModel):
    Id: Final[UserID]
    Bonus: PositiveFloat

    model_config: ConfigDict = ConfigDict(frozen=True)

    @field_validator("Bonus", mode="before")
    def bonus_validator(cls: BonusEvent, value: float) -> Optional[float]:
        if value <= 0:
            raise AmountError()
        return value