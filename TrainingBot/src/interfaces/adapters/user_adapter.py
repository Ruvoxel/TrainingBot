from typing import Literal, Optional

from ..ports import portUserRepository
from ...domain import UserID, User

class adapterUserRepository(portUserRepository):
    def __init__(self: adapterUserRepository) -> adapterUserRepository:
        self.BD: dict[UserID, User] = {}

    def getUserByID(self: adapterUserRepository, userID: UserID) -> Optional[User]:
        return self.BD.get(userID)
    
    def getUserALL(self: adapterUserRepository, mode: Literal["all", "username"]) -> list[User]:
        if mode == "all":
            return self.BD.values()
        elif mode == "username":
            return filter(lambda user: user.TelegramUsername != None, self.BD.values())
        
    
    def saveUser(self: adapterUserRepository, user: User) -> Optional[User]:
        self.BD[user.TelegramID] = user
        
        return self.getUserByID(user.TelegramID)