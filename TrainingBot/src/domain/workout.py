from pydantic import BaseModel, field_validator
from pydantic.config import ConfigDict
from typing import Union

from .enums import WorkoutType, WorkoutDay
from .errors import notTypeFoundError

class Workout(BaseModel):
    Title: str
    Callories: float
    Type: WorkoutType
    Day: WorkoutDay
    WorkoutTime: float
    Exercises: tuple[str, ...] = ()

    model_config: ConfigDict = ConfigDict(frozen=True)

    def addExercise(self: Workout, exercise: Union[str, list]) -> Workout:
        return Workout(
            Title=self.Title,
            Callories=self.Callories,
            Type=self.Type,
            Day=self.Day,
            WorkoutTime=self.WorkoutTime,
            Exercises=self.Exercises + (exercise,) if isinstance(exercise, str) else (_exercise for _exercise in exercise)
        )
    
    @field_validator("Type", mode="before")
    def type_validator(cls, number: int) -> WorkoutType:
        if isinstance(number, WorkoutType): return number
        
        match number:
            case 1: return WorkoutType.POWER
            case 2: return WorkoutType.FITNES
            case 3: return WorkoutType.WEIGHT_LOSS
            case _: raise notTypeFoundError()

    @field_validator("Day", mode="before")
    def day_validator(cls, number: int) -> WorkoutDay:
        if isinstance(number, WorkoutDay): return number
        
        match number:
            case 1: return WorkoutDay.MONDAY
            case 2: return WorkoutDay.TUESDAY
            case 3: return WorkoutDay.WEDNESDAY
            case 4: return WorkoutDay.THURSDAY
            case 5: return WorkoutDay.FRIDAY
            case 6: return WorkoutDay.SATURDAY
            case 7: return WorkoutDay.SUNDAY
            case _: raise notTypeFoundError()

    def __str__(self) -> str:
        return f"""( День: {self.Title} | Сженые калории: {self.Callories} | Тип тренировки: {self.Type} | День тренировки: {self.Day} | Время тренировки: {self.WorkoutTime}
            Упражнения => Численость: {len(self.Exercises)} | Сами упражнения: {" ".join(f"Упр: {exercise}" for exercise in filter(lambda _exercise: _exercise != "", self.Exercises))}
        )"""
    
    