from typing import Optional
from datetime import datetime
from random import randint

from src.interfaces.ports import portUserRepository, portGiveRepository, portWorkoutListRepository
from src.domain.base_events.base import EventHandler
from src.domain.base_events.event import RegisterUserEnvents, BonusEvent, DayliEvent, createWorkoutEvent, createWorkoutListEvent
from src.domain import User, UserID, Give, WorkoutList, Workout
from src.domain.errors import UserError, notBonusError, TexError, WorkoutListError, moreDayError, GiveError, ResponseError, notTypeFoundError
from src.unit_of_work import GlobalUOW

class Service():
    def __init__(self: Service, userRepository: portUserRepository, giveRepository: portGiveRepository, workout_listRepository: portWorkoutListRepository) -> Service:
        self.userRepository: portUserRepository = userRepository
        self.giveRepository: portGiveRepository = giveRepository
        self.workout_listRepository: portWorkoutListRepository = workout_listRepository

        self.eventHandler: EventHandler = EventHandler()
        self.UOW: GlobalUOW = GlobalUOW()

    def registerUser(self: Service, telegram_id: UserID, telegram_username: Optional[str]=None) -> None:
        try:
            _User: User = self.userRepository.getUserByID(telegram_id)
            if not _User is None:
                print(1)
                raise UserError()
            
            with self.UOW:
                people: User = User(TelegramID=telegram_id, TelegramUsername=telegram_username)
                _User: User = self.userRepository.saveUser(people)

                if not _User is None:
                    with self.eventHandler as handler:
                        event: RegisterUserEnvents = RegisterUserEnvents(Id=telegram_id)
                        handler(event)

                        return
                raise UserError()        
        
        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()
        
    
    def giveBonus(self: Service, telegram_id: UserID) -> None:
        try:
            _User: User = self.userRepository.getUserByID(telegram_id)
            if _User is None:
                raise UserError()
            
            with self.UOW:
                _Bonus: BonusEvent = BonusEvent(Id=telegram_id, Bonus=300)
                _Give: Give = Give(Id=_Bonus.Id, Amount=_Bonus.Bonus, Date=datetime.now())
                if _User.Bonus:
                    with self.eventHandler as handler:
                        handler(_Bonus)
                        newUser: User = _User.Payment(_Give)
                        
                        _new: User = newUser.cantBonus()
                        self.userRepository.saveUser(_new)
                        self.giveRepository.saveGive(_Give)

                elif sum(workout_list.TotalCallories for workout_list in self.workout_listRepository.getWorkoutListByID(telegram_id)) >= 5000:
                    _Dayli: DayliEvent = DayliEvent(Id=telegram_id, TotalCalories=sum(workout_list.TotalCallories for workout_list in self.workout_listRepository.getWorkoutListByID(telegram_id)))
                    _Give: Give = Give(Id=telegram_id, Amount=600, Date=datetime.now())

                    with self.eventHandler as handler:
                        handler(_Dayli)
                        _User: User = _User.Payment(_Give)
                        
                        for _workout_list in self.workout_listRepository.getWorkoutListByID(telegram_id):
                            _new: WorkoutList = _workout_list.clearWorkout()
                            self.workout_listRepository.saveWorkoutList(_new)

                        self.userRepository.saveUser(_User)
                        self.giveRepository.saveGive(_Give)
                else:
                    raise notBonusError()      
        
        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()
        
    def createWorkout(self: Service, telegram_id: UserID) -> None:    
        try:
            _User: User = self.userRepository.getUserByID(telegram_id)
            if _User is None:
                raise UserError()

            with self.UOW:
                _WorkoutList: list[WorkoutList] = self.workout_listRepository.getWorkoutListByID(telegram_id)

                if len(_WorkoutList) == 0:
                    raise WorkoutListError()
                
                for index, workout in enumerate(_WorkoutList):
                    print(f"{index + 1} - {str(workout)}")
                Index: int = int(input("Введите номер недели, куда Вы хотите добавить этот день ( Пример: 1; 2 )\nНомер: ")) - 1

                if Index < 0:
                    raise ResponseError()
                
                try:
                    _getWorkoutList: WorkoutList = _WorkoutList[Index]
                except IndexError:
                    raise notTypeFoundError()

                if len(_getWorkoutList) == 7:
                    raise moreDayError()

                _Workout: Workout = Workout(
                    Title=input("Введите название тренировки (Пример: День Груди)\nНазвание: "),
                    Callories=int(input("Введите число колорий ( Пример: 2300; 4500 )\nЧисло: ")),
                    Type=int(input("Введите число типа ( Пример: 1 - Силовая; 2 - Фитнес; 3 - Снежение веса )\nЧисло типа: ")),
                    Day=int(input("Введите число дня ( Пример: 1 - Понедельник; 2 - Вторник; так делее )\nЧисло дня: ")),
                    WorkoutTime=float(input("Введите время тренировки ( Пример: 2.5 (2часа и 30мин); 3.0 (3часа) )\nВремя: ")),
                    Exercises=()
                ).addExercise(input("Введите упражнения, которые вы полняли, но соблюдайте отступы пернед новыйм упражнением ( Пример: Тяга-блока Присед-с-штангой )\nУпражнения: ").split(" "))
                
                with self.eventHandler as handler:
                    event: createWorkoutEvent = createWorkoutEvent(Id=telegram_id)
                    handler(event)
                    
                    _newWorkoutList: WorkoutList = _getWorkoutList.addWorkout(_Workout)
                    self.workout_listRepository.saveWorkoutList(_newWorkoutList)
        
        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()
    
    def createWorkoutList(self: Service, telegram_id: UserID) -> None:
        try:
            _User: User = self.userRepository.getUserByID(telegram_id)
            if _User is None:
                raise UserError()

            with self.UOW:
                _WorkoutList: WorkoutList = WorkoutList(
                    Id=randint(1000, 9999),
                    User=_User,
                    Workouts=(),
                    Description=input("Введите описание своей недели ( пример: Хочу повыполнять еждевные задачи )\nОписание: "),
                    Date=datetime.now()
                )

                with self.eventHandler as handler:
                    events: createWorkoutListEvent = createWorkoutListEvent(Id=telegram_id)
                    handler(events)

                    self.workout_listRepository.saveWorkoutList(_WorkoutList)

        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()
        
    def getMyGives(self: Service, telegam_id: UserID) -> None:
        try:
            _User: User = self.userRepository.getUserByID(telegam_id)
            if _User is None:
                raise UserError()
            
            with self.UOW:
                _Gives: list[Give] = self.giveRepository.getGiveByID(telegam_id)

                if len(_Gives) == 0:
                    raise GiveError()

                for _Give in _Gives:
                    print(f"ID подарка (ваш): {_Give.Id}\nСумма подарка: {_Give.Amount}\nДата получения подарка: {_Give.Date}")
        
        except Exception as error:
            if getattr(error, "server", False):
                raise
            raise TexError()