from pytest import raises

from src.domain import User
from src.domain.errors import UsernameError, AmountError
from src.domain import Give

def test_create_user_vallid() -> None:
    _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")

    assert _User.TelegramID == 734829156
    assert _User.TelegramUsername == "@LoveGeer"
    assert _User.Balance == 0

def test_create_user_not_vallid() -> None:
    with raises(UsernameError) as exc:
        _User: User = User(TelegramID=734829156, TelegramUsername="LoveGeer")
    
    assert "Невалидное имя." in str(exc.value)

def test_give_user_vallid():
    _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")
    _Give: Give = Give(Id=1, Amount=200)

    newUser = _User.Payment(give=_Give)

    assert newUser.Balance == 200

def test_give_user_not_vallid() -> None:
    _User: User = User(TelegramID=734829156, TelegramUsername="@LoveGeer")

    with raises(AmountError) as exc:
        _Give: Give = Give(Id=1, Amount=-200)

    assert "Сумма должна быть положительным числом." in str(exc.value)