from datetime import datetime
from pytest import raises

from src.domain import WorkoutList, Workout
from src.domain.enums import WorkoutType, WorkoutDay
from src.domain import User
from src.domain.errors import NotWorkoutError 

def createWorkout(title: str, callories: float, type: WorkoutType, day: WorkoutDay, workout_time: float, exercises: tuple[str, ...] = ()) -> Workout:
    return Workout(
        Title=title,
        Callories=callories,
        Type=type,
        Day=day,
        WorkoutTime=workout_time,
        Exercises=exercises
    )

def test_total_callories_and_time() -> None:
    Monday: Workout = createWorkout("Вверх", 100, WorkoutType.POWER, WorkoutDay.MONDAY, 2.5)
    Sunday: Workout = createWorkout("Низ", 200, WorkoutType.POWER, WorkoutDay.SUNDAY, 2.5)
    Friday: Workout = createWorkout("Вверх", 300, WorkoutType.POWER, WorkoutDay.FRIDAY, 2.5)

    _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")
    Date: datetime = datetime.now()
    _WorkoutList: WorkoutList = WorkoutList(Id=1, User=_User, Description="Силовая Неделя", Date=Date)
    
    newWorkoutList: WorkoutList = _WorkoutList.addWorkout([Monday, Sunday, Friday])

    assert len(newWorkoutList) == 3
    assert newWorkoutList.TotalCallories == 600
    assert newWorkoutList.TotalTime == 2.5
    assert newWorkoutList.Date == Date

def test_clear_workout() -> None:
    Monday: Workout = createWorkout("Вверх", 100, WorkoutType.POWER, WorkoutDay.MONDAY, 2.5)
    Sunday: Workout = createWorkout("Низ", 200, WorkoutType.POWER, WorkoutDay.SUNDAY, 2.5)
    Friday: Workout = createWorkout("Вверх", 300, WorkoutType.POWER, WorkoutDay.FRIDAY, 2.5)

    _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")
    Date: datetime = datetime.now()
    _WorkoutList: WorkoutList = WorkoutList(Id=1, User=_User, Description="Силовая Неделя", Date=Date)
    
    newWorkoutList: WorkoutList = _WorkoutList.addWorkout([Monday, Sunday, Friday])
    clearWorkoutList: WorkoutList = newWorkoutList.clearWorkout()

    assert len(clearWorkoutList) == 0
    assert clearWorkoutList.TotalCallories == 0
    
    with raises(NotWorkoutError) as exc:
        clearWorkoutList.TotalTime

    assert "Не найдено тренажерных дней." in str(exc.value)
    assert clearWorkoutList.Date == Date