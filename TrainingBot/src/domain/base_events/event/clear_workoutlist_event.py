from pydantic import BaseModel
from pydantic.config import ConfigDict
from typing import Final

from ...user import UserID

class ClearWorkoutListEvent(BaseModel):
    Id: Final[UserID]

    model_config: ConfigDict = ConfigDict(frozen=True)