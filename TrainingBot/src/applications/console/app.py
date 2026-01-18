from typing import Optional, Final, Literal
from os import system

from src.services import Service
from src.interfaces.adapters import adapterUserRepository, adapterWorkoutListRepository, adapterGiveRepository
from src.domain import UserID, User, WorkoutList
from src.domain.errors import TexError, UserError, WorkoutListError, ResponseError, NotWorkoutError, ResponseError, notTypeFoundError
from src.domain.base_events.event import ClearWorkoutListEvent
from src.domain.enums import AppStatus

class Applications():
    Service: Final[Optional[Service]] = None
    Movement: Literal["Получить Бонус", "Создать День", "Создать Неделю", "Посмотреть свои подарки", "Посмотреть Недели", "Очистить Неделю", "Посмотреть Монеты"]
    Status: AppStatus = AppStatus.NO_DEFINED

    def stream(self: Applications) -> Applications:
        self.Service: Service = Service(
            userRepository=adapterUserRepository(),
            giveRepository=adapterGiveRepository(),
            workout_listRepository=adapterWorkoutListRepository()
        )
        self.Status: AppStatus = AppStatus.START

        return self
    
    def start(self: Applications, telegram_id: UserID) -> None:
        try:
            with self.Service.UOW:
                if self.Status == AppStatus.START:
                    system("cls")
                    self.Id: UserID = telegram_id
                    Username: Optional[str] = input("Введите ваше Имя: ") or None

                    self.Service.registerUser(telegram_id=self.Id, telegram_username=Username)

                movement_list: list[str] = ["Получить Бонус", "Создать День", "Создать Неделю", "Посмотреть свои подарки", "Посмотреть Недели", "Очистить Неделю", "Посмотреть Монеты"]
                for index, _movement in enumerate(movement_list):
                    print(f"{index + 1} - {_movement}")
                
                try:
                    print("\n\nДля остоновки отправьте пустую строку.")
                    movement: int = int(input("Выбери действие: ")) - 1

                    if movement < 0:
                        raise ResponseError()
                    elif movement + 1 > len(movement_list):
                        raise notTypeFoundError()
                    

                except ValueError:
                    self.Status: AppStatus = AppStatus.STOP
                    raise 
                
                self.Movement = movement_list[movement]

        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()
    
    def clearWorkoutList(self: Applications, telegram_id: UserID) -> None:
        try:
            with self.Service.UOW:
                _WorkoutList: list[WorkoutList] = self.Service.workout_listRepository.getWorkoutListByID(telegram_id)
                
                if len(_WorkoutList) < 1:
                    raise WorkoutListError() 

                for index, workoutlist in enumerate(_WorkoutList):
                    print(f"{index + 1} - {str(workoutlist)}")
                Index: int = int(input("Какой удалить? ( Пример: 1; 2 )\nНомер: ")) - 1
                
                if Index < 0:
                    raise ResponseError()

                try:
                    _getWorkoutList: WorkoutList = _WorkoutList[Index]
                except IndexError:
                    raise notTypeFoundError()            
                
                if len(_getWorkoutList) == 0:
                    raise NotWorkoutError()

                with self.Service.eventHandler as handler:
                    event: ClearWorkoutListEvent = ClearWorkoutListEvent(Id=telegram_id)
                    handler(event)

                    newWorkoutList: list[WorkoutList] = _getWorkoutList.clearWorkout()
                    self.Service.workout_listRepository.saveWorkoutList(newWorkoutList)
        
        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()
        
    def checkMoney(self: Applications, telegram_id: UserID) -> None:
        try:
            with self.Service.UOW:
                _User: Optional[User] = self.Service.userRepository.getUserByID(telegram_id)
                if not _User:
                    raise UserError()
                
                print(f"У вас {_User.Balance} монет(ы)")

        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()
    
    def getWorkoutList(self: Applications, telegram_id: UserID) -> None:
        try:
            with self.Service.UOW:
                _WorkoutList: list[WorkoutList] = self.Service.workout_listRepository.getWorkoutListByID(telegram_id)

                if len(_WorkoutList) == 0:
                    raise WorkoutListError()

                for index, workout in enumerate(_WorkoutList):
                    print(f"{index + 1} - {str(workout)}")
                Index: int = int(input("\n\nВы можете посмотреть дни в каждом из недели, просто напишите его номер ( Пример 1; 2; 0 - это обратно )\nНомер: "))
                
                if Index < 0:
                    raise ResponseError()
                elif Index == 0:
                    self.Status = AppStatus.BACK
                    return
                Index -= 1
                
                try:
                    _getWorkoutList: WorkoutList = _WorkoutList[Index]
                except IndexError:
                    raise notTypeFoundError()

                if len(_getWorkoutList) == 0:
                    raise NotWorkoutError()

                for index, workout in enumerate(_getWorkoutList.Workouts):
                    print(f"{index + 1} - {str(workout)}")
                print(f"\n\nОбщее количество калорий: {_WorkoutList[Index].TotalCallories} | Cреднее времени: {_WorkoutList[Index].TotalTime}")

        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()