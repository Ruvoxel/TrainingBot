from pydantic import BaseModel
from pydantic.config import ConfigDict
from typing import Final, Optional, Union, NewType
from datetime import datetime

from .user import User
from .workout import Workout
from .errors import NotWorkoutError

WorkoutID = NewType("WorkoutID", int)

class WorkoutList(BaseModel):
    Id: Final[WorkoutID]
    User: Final[User]
    Workouts: tuple[Workout, ...] = ()
    Description: Optional[str] = None
    Date: datetime 

    model_config: ConfigDict = ConfigDict(frozen=True)

    def addWorkout(self: WorkoutList, workout: Union[Workout, list[Workout]]) -> WorkoutList:               
        return WorkoutList(
            Id=self.Id,
            User=self.User,
            Workouts=self.Workouts + tuple(workout) if isinstance(workout, list) else self.Workouts + (workout,),
            Description=self.Description,
            Date=self.Date
        )
    
    def clearWorkout(self: WorkoutList) -> WorkoutList:
        return WorkoutList(
            Id=self.Id,
            User=self.User,
            Workouts=(),
            Description=self.Description,
            Date=self.Date
        )
    
    @property
    def TotalCallories(self: WorkoutList) -> float:
        return sum(Workout.Callories for Workout in self.Workouts)
    
    @property
    def TotalTime(self: WorkoutList) -> float:
        try:
            return sum(Workout.WorkoutTime for Workout in self.Workouts) / len(self)
        except ZeroDivisionError:
            raise NotWorkoutError()
    
    def __len__(self: WorkoutList) -> int:
        return len(self.Workouts)
    
    def __str__(self: WorkoutList) -> str:
        return f"Неделя под ID: {self.Id}"
    
    
    
    