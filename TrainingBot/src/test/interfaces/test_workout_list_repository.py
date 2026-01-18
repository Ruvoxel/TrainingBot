from datetime import datetime
from typing import Optional

from src.interfaces.ports import portWorkoutListRepository
from src.domain import WorkoutList, Workout, User, UserID
from src.domain.enums import WorkoutType, WorkoutDay

class FakeRepository(portWorkoutListRepository):
    def __init__(self: FakeRepository) -> FakeRepository:
        Monday: Workout = Workout(Title="Вверх", Callories=300, Type=WorkoutType.POWER, Day=WorkoutDay.MONDAY, WorkoutTime=2.5)
        Sunday: Workout = Workout(Title="Вверх", Callories=400, Type=WorkoutType.POWER, Day=WorkoutDay.SUNDAY, WorkoutTime=2.5)
        Tuesday: Workout = Workout(Title="Вверх", Callories=700, Type=WorkoutType.POWER, Day=WorkoutDay.TUESDAY, WorkoutTime=2.5)

        _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")
        Time: datetime = datetime.now()

        oneWeek: WorkoutList = WorkoutList(Id=1, User=_User, Description="Силовая тренировка", Date=Time, Workouts=(Monday, Sunday, Tuesday))
        twoWeek: WorkoutList = WorkoutList(Id=2,User=_User, Description="Силовая тренировка", Date=Time, Workouts=(Monday, Sunday, Tuesday))
        
        self.DB: list[dict[UserID, WorkoutList]] = [{oneWeek.User.TelegramID: oneWeek}, {twoWeek.User.TelegramID: twoWeek}]

    def getWorkoutListByID(self: FakeRepository, userID: UserID) -> Optional[list[WorkoutList]]:
        return list(map(lambda item: item.get(userID), list(filter(lambda item: list(item.keys())[0] == userID, self.DB))))
    
    def saveWorkoutList(self: FakeRepository, workout_list: WorkoutList) -> Optional[list[WorkoutList]]:
        if isinstance(workout_list, list):
            for workout in workout_list:
                userID: UserID = workout.User.TelegramID
                _WorkoutList: WorkoutList = list(filter(lambda item: item.Id == workout.Id, self.getWorkoutListByID(userID)))[0]
                Index: int = self.DB.index({userID: _WorkoutList})
                self.DB[Index] = {userID: workout}

                return self.getWorkoutListByID(userID)
        else:
            userID: UserID = workout_list.User.TelegramID
            _WorkoutList: WorkoutList = list(filter(lambda item: item.Id == workout_list.Id, self.getWorkoutListByID(userID)))[0]
            Index: int = self.DB.index({userID: _WorkoutList})
            self.DB[Index] = {userID: workout_list}

            return self.getWorkoutListByID(userID)
    
fake_repository: FakeRepository = FakeRepository()

def test_get_workoutlist() -> None:
    _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")
    workoutlist: list[WorkoutList] = fake_repository.getWorkoutListByID(_User.TelegramID)

    assert len(workoutlist) == 2

def test_get_all_workoutlist() -> None:
    _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")
    workoutlist: list[WorkoutList] = fake_repository.getWorkoutListByID(_User.TelegramID)

    oneWorkout: WorkoutList = workoutlist[0]
    twoWorkout: WorkoutList = workoutlist[1]

    assert oneWorkout != twoWorkout
    assert oneWorkout.TotalCallories == twoWorkout.TotalCallories
    assert oneWorkout.TotalTime == 2.5 and twoWorkout.TotalTime == 2.5

def test_add_workout() -> None:
    _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")
    workoutlist: list[WorkoutList] = fake_repository.getWorkoutListByID(_User.TelegramID)
    
    Friday: Workout = Workout(Title="Вверх", Callories=700, Type=WorkoutType.POWER, Day=WorkoutDay.FRIDAY, WorkoutTime=2.5)

    oneWorkout: WorkoutList = workoutlist[0]
    _: WorkoutList = workoutlist[1]
    replace: WorkoutList = oneWorkout.addWorkout(Friday)

    newWorkoutlist: list[WorkoutList] = fake_repository.saveWorkoutList(replace)

    assert len(newWorkoutlist[0].Workouts) == 4