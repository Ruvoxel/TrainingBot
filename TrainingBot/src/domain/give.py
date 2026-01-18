from pydantic import BaseModel, PositiveFloat, field_validator
from pydantic.config import ConfigDict
from typing import Final, NewType, Optional
from datetime import datetime

from .errors import AmountError

GiveID = NewType("GiveID", int)

class Give(BaseModel):
    Id: Final[GiveID]
    Amount: PositiveFloat
    Date: datetime = datetime.now()

    model_config: ConfigDict = ConfigDict(frozen=True)

    @field_validator("Amount", mode="before")
    def AmountValidator(cls: Give, value: float) -> Optional[float]:
        if value <= 0:
            raise AmountError()
        return value