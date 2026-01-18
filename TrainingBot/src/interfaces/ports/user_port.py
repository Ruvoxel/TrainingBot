from typing import Literal, Optional
from abc import ABC, abstractmethod

from ...domain import User, UserID

class portUserRepository(ABC):

    @abstractmethod
    def getUserByID(self, userID: UserID) -> Optional[User]:
        raise NotImplementedError("[Ошибка Метода | Нужно переопределить] -> Метод для получения пользователя по его ID.")

    @abstractmethod
    def getUserALL(self, mode: Literal["all", "username"]) -> list[User]:
        raise NotImplementedError("[Ошибка Метода | Нужно переопределить] -> Метод для получения всех пользователей.")

    @abstractmethod
    def saveUser(self, user: User) -> Optional[User]:
        raise NotImplementedError("[Ошибка Метода | Нужно переопределить] -> Метод для сохранения пользователя.")