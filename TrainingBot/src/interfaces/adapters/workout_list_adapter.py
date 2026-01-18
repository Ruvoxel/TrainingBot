from typing import Optional, Union, Final
from traceback import print_exc

from ..ports import portWorkoutListRepository
from ...domain import UserID, WorkoutList, WorkoutID

class adapterWorkoutListRepository(portWorkoutListRepository):
    def __init__(self: adapterWorkoutListRepository) -> adapterWorkoutListRepository:
        self.DB: list[dict[WorkoutID, WorkoutList]] = []

    def getWorkoutListByID(self: adapterWorkoutListRepository, userID: UserID) -> Optional[list[WorkoutList]]:
        filters: list[dict[UserID, WorkoutList]] = list(filter(lambda item: list(item.values())[0].User.TelegramID == userID if item != [] else False, self.DB))
        return list(map(lambda item: list(item.values())[0], filters))
        
    
    def saveWorkoutList(self, workout_list: Union[list[WorkoutList], WorkoutList]) -> Optional[list[WorkoutList]]:
        if isinstance(workout_list, list):
            for workout in workout_list:
                Id: Final[UserID] = workout.Id
                filters: list[dict[UserID, WorkoutList]] = list(filter(lambda item: list(item.keys())[0] == Id if item != {} else False, self.DB))
                try:
                    Index: int = self.DB.index(filters[0] if len(filters) > 0 else filters)
                    filters[Index][Id] = workout
                except ValueError:
                    filters.append({Id: workout})
                    self.DB.append(filters[0])
                
        else:
            Id: Final[WorkoutID] = workout_list.Id
            filters: list[dict[UserID, WorkoutList]] = list(filter(lambda item: list(item.keys())[0] == Id if item != {} else False, self.DB))
            try:
                Index: int = self.DB.index(filters[0] if len(filters) > 0 else filters)
                self.DB[Index][Id] = workout_list
            except ValueError:
                filters.append({Id: workout_list})
                self.DB.append(filters[0])
