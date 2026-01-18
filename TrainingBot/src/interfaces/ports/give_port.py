from typing import Optional
from abc import ABC, abstractmethod

from ...domain import Give, GiveID

class portGiveRepository(ABC):

    @abstractmethod
    def getGiveByID(self: portGiveRepository, giveID: GiveID) -> Optional[Give]:
        raise NotImplementedError("[Ошибка Метода | Нужно переопределить] -> Метод для получения подарка по его ID.")

    @abstractmethod    
    def saveGive(self: portGiveRepository, give: Give) -> Optional[Give]:
        raise NotImplementedError("[Ошибка Метода | Нужно переопределить] -> Метод для сохранения подарка.")