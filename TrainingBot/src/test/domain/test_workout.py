from src.domain import Workout
from src.domain.enums import WorkoutType, WorkoutDay

def test_create_workout_not_notes() -> None:
    _Workout: Workout = Workout(Id=1, Title="Вверх", Callories=300, Type=WorkoutType.POWER, Day=WorkoutDay.MONDAY, WorkoutTime=2.5)

    assert _Workout.Title == "Вверх"
    assert _Workout.Callories == 300
    assert _Workout.Type == WorkoutType.POWER
    assert _Workout.Day == WorkoutDay.MONDAY
    assert _Workout.WorkoutTime == 2.5

def test_create_workout_notes() -> None:
    _Workout: Workout = Workout(Id=1, Title="Низ", Callories=300, Type=WorkoutType.POWER, Day=WorkoutDay.MONDAY, WorkoutTime=2.5, Exercises=("Жим плотформы", "Румынская тяга", "Болгарские выпады", "Икры"))

    assert _Workout.Title == "Низ"
    assert _Workout.Callories == 300
    assert _Workout.Type == WorkoutType.POWER
    assert _Workout.Day == WorkoutDay.MONDAY
    assert _Workout.WorkoutTime == 2.5
    assert _Workout.Exercises == ("Жим плотформы", "Румынская тяга", "Болгарские выпады", "Икры")

def test_create_workout_notes_add() -> None:
    _Workout: Workout = Workout(Id=1, Title="Низ", Callories=300, Type=WorkoutType.POWER, Day=WorkoutDay.MONDAY, WorkoutTime=2.5, Exercises=("Жим плотформы", "Румынская тяга", "Болгарские выпады", "Икры"))
    newWorkout = _Workout.addExercise("Растяжка")

    assert newWorkout.Title == "Низ"
    assert newWorkout.Callories == 300
    assert newWorkout.Type == WorkoutType.POWER
    assert newWorkout.Day == WorkoutDay.MONDAY
    assert newWorkout.WorkoutTime == 2.5
    assert newWorkout.Exercises == ("Жим плотформы", "Румынская тяга", "Болгарские выпады", "Икры", "Растяжка")