from pydantic import BaseModel, PositiveFloat, field_validator
from pydantic.config import ConfigDict
from typing import NewType, Final, Optional

from .give import Give
from .errors import UsernameError

UserID = NewType("UserID", int)

class User(BaseModel):
    TelegramID: Final[UserID]
    TelegramUsername: Optional[str] = None
    Balance: PositiveFloat = 0
    Bonus: bool = True

    model_config: ConfigDict = ConfigDict(frozen=True)

    def Payment(self: User, give: Give) -> User:
        return User(
            TelegramID=self.TelegramID,
            TelegramUsername=self.TelegramUsername,
            Balance=self.Balance + give.Amount,
            Bonus=self.Bonus
        )
    
    def cantBonus(self: User) -> User:
        return User(
            TelegramID=self.TelegramID,
            TelegramUsername=self.TelegramUsername,
            Balance=self.Balance,
            Bonus=False
        )
    
    @field_validator("TelegramUsername")
    def ValidatorUsername(cls, v: str) -> Optional[str]:
        if v is None: return None
        if not v.startswith("@"): raise UsernameError()
        return v
