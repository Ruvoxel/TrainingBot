from typing import Optional, Type
from types import TracebackType

from .base_envents import BaseEnvents, Class
from ..event import RegisterUserEnvents, BonusEvent, DayliEvent, createWorkoutEvent, createWorkoutListEvent, ClearWorkoutListEvent

@BaseEnvents
class EventHandler:
    Base: Optional[BaseEnvents] = None

    @BaseEnvents.setEnvent(RegisterUserEnvents)
    def RegisterEvent(self: EventHandler) -> None:
        print("Вы добавлены! Добро пожаловать в наш сервис.")

    @BaseEnvents.setEnvent(BonusEvent)
    def addBonus(self: EventHandler) -> None:
        print("Поздровляем! Вы получили бесплатно 300 рублей.")

    @BaseEnvents.setEnvent(DayliEvent)
    def dayli(self: EventHandler) -> None:
        print("Вы выполнили ежедневку! Вы набрали ровно/больше 5.000 калорий.")

    @BaseEnvents.setEnvent(createWorkoutListEvent)
    def create_workout_list(self: EventHandler) -> None:
        print("Вы успешно создали новую неделю!")

    @BaseEnvents.setEnvent(createWorkoutEvent)
    def create_workout(self: EventHandler) -> None:
        print("Вы успешно создали новый день!")

    @BaseEnvents.setEnvent(ClearWorkoutListEvent)
    def clear_workoutlist(self: EventHandler) -> None:
        print("Вы успешно очистили свою неделю!")

    def __enter__(self: Type[Class]) -> callable:
        return self.Base.__enter__()
    
    def __exit__(self: Type[Class], exc_type: type[BaseException], exc_value: Optional[BaseEnvents], traceback: TracebackType) -> None:
        return self.Base.__exit__(exc_type, exc_value, traceback)
