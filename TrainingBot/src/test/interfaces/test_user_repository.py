from typing import Optional, Literal
from datetime import datetime

from src.interfaces.ports import portUserRepository
from src.domain import User, UserID, Give

class FakeRepository(portUserRepository):
    def __init__(self: FakeRepository) -> FakeRepository:
        oneUser: User = User(TelegramID=1111111, TelegramUsername="@GoalRonaldo")
        twoUser: User = User(TelegramID=2222222, TelegramUsername="@GoalMessi")
        threeUser: User = User(TelegramID=3333333)

        self.BD: dict[UserID, User] = {oneUser.TelegramID: oneUser, twoUser.TelegramID: twoUser, threeUser.TelegramID: threeUser}

    
    def getUserByID(self: FakeRepository, userID: UserID) -> Optional[User]:
        return self.BD.get(userID)
    
    def getUserALL(self: FakeRepository, mode: Literal["all", "username"]) -> list[User]:
        if mode == "all":
            return list(self.BD.values())
        elif mode == "username":
            return list(filter(lambda user: user.TelegramUsername != None, self.BD.values()))
        
    
    def saveUser(self: FakeRepository, user: User) -> Optional[User]:
        self.BD[user.TelegramID] = user
        
        return self.getUserByID(user.TelegramID)

fake_repository: FakeRepository = FakeRepository()

def test_get_user() -> None:
    _User: User = User(TelegramID=1111111, TelegramUsername="@GoalRonaldo")
    newUser: User = fake_repository.getUserByID(userID=_User.TelegramID)

    assert _User.TelegramID == newUser.TelegramID
    assert _User.TelegramUsername == newUser.TelegramUsername

def test_get_all() -> None:
    _oneUser: User = User(TelegramID=1111111, TelegramUsername="@GoalRonaldo")
    _twoUser: User = User(TelegramID=2222222, TelegramUsername="@GoalMessi")
    _threeUser: User = User(TelegramID=3333333)

    list_users: list = [_oneUser, _twoUser, _threeUser]

    assert fake_repository.getUserALL(mode="all") == list_users

def test_get_username() -> None:
    _oneUser: User = User(TelegramID=1111111, TelegramUsername="@GoalRonaldo")
    _twoUser: User = User(TelegramID=2222222, TelegramUsername="@GoalMessi")

    list_users: list = [_oneUser, _twoUser]

    assert fake_repository.getUserALL(mode="username") == list_users

def test_update_user_and_check_your_data() -> None:
    _User: User = User(TelegramID=4444444, TelegramUsername="@PickachuTEA").Payment(give=Give(Id=111, Amount=200, Date=datetime.now()))
    _oneUser: User = User(TelegramID=1111111, TelegramUsername="@GoalRonaldo")
    _twoUser: User = User(TelegramID=2222222, TelegramUsername="@GoalMessi")
    _threeUser: User = User(TelegramID=3333333)
    fake_repository.saveUser(user=_User)

    list_users: list = [_oneUser, _twoUser, _threeUser, _User]
    assert fake_repository.getUserALL(mode="all") == list_users
    list_users.remove(_threeUser)
    assert fake_repository.getUserALL(mode="username") == list_users
    
    newUser: User = _User.Payment(Give(Id=222, Amount=300, Date=datetime.now()))
    fake_repository.saveUser(newUser)
    user: User = fake_repository.getUserByID(newUser.TelegramID)
    
    assert user.Balance == 500