from pydantic import BaseModel
from pydantic.config import ConfigDict
from typing import Final

from src.domain import UserID

class RegisterUserEnvents(BaseModel):
    Id: Final[UserID]

    model_config: ConfigDict = ConfigDict(frozen=True)