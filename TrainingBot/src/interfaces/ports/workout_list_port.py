from typing import Optional, Union
from abc import ABC, abstractmethod

from ...domain import UserID, WorkoutList

class portWorkoutListRepository(ABC):
    
    @abstractmethod
    def getWorkoutListByID(self, userID: UserID) -> Optional[Union[list[WorkoutList], WorkoutList]]:
        raise NotImplementedError("[Ошибка Метода | Нужно переопределить] -> Метод для получения тренерской недели по ID пользователя.")

    @abstractmethod
    def saveWorkoutList(self, workout_list: WorkoutList) -> WorkoutList:
        raise NotImplementedError("[Ошибка Метода | Нужно переопределить] -> Метод для сохранения тренерской недели.")