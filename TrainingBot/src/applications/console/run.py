from os import system
from typing import Final

from .app import Applications
from src.domain.enums import AppStatus
from src.domain import UserID
from src.domain.errors import UsernameError

if __name__ == "__main__":
    App: Applications = Applications().stream()
    TelegramID: Final[UserID] = 37922723
    
    while True:
        try:
            if App.Status != AppStatus.ERROR and App.Status != AppStatus.IN_PROGRESS:
                
                if App.Status == AppStatus.START:
                    App.start(telegram_id=TelegramID)
                
                if App.Movement == "Посмотреть Монеты":
                    App.checkMoney(telegram_id=App.Id)
                
                if App.Movement == "Получить Бонус":
                    App.Service.giveBonus(telegram_id=App.Id)
                
                if App.Movement == "Создать День":
                    App.Service.createWorkout(telegram_id=App.Id)
                
                if App.Movement == "Создать Неделю":
                    App.Service.createWorkoutList(telegram_id=App.Id)
                
                if App.Movement == "Посмотреть свои подарки":
                    App.Service.getMyGives(telegam_id=App.Id)

                if App.Movement == "Очистить Неделю":
                    App.clearWorkoutList(telegram_id=App.Id)

                if App.Movement == "Посмотреть Недели":
                    App.getWorkoutList(telegram_id=App.Id)

                App.Status = AppStatus.IN_PROGRESS

            elif App.Status == AppStatus.IN_PROGRESS or App.Status == AppStatus.ERROR:
                App.Status = AppStatus.NO_DEFINED

                print("\n\n")
                system("pause")
                system("cls")
                App.start(telegram_id=App.Id or TelegramID)

        except Exception as e:
            if any(list(filter(lambda error: type(error) == type(UsernameError()) if App.Service.userRepository.getUserByID(App.Id or TelegramID) is None else False, App.Service.UOW.errors))):
                print("\n\n")
                system("pause")
                continue
            
            if App.Status == AppStatus.STOP:
                break
            App.Status = AppStatus.ERROR
            continue
            
            