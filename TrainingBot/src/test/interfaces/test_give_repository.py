from typing import Optional
from datetime import datetime

from src.interfaces.ports import portGiveRepository
from src.domain import Give, GiveID

class FakeRepository(portGiveRepository):
    def __init__(self: FakeRepository) -> FakeRepository:
        oneGive: Give = Give(Id=111, Amount=100, Date=datetime.now())
        towGive: Give = Give(Id=222, Amount=300, Date=datetime.now())
        threeGive: Give = Give(Id=333, Amount=600, Date=datetime.now())

        self.DB: dict[GiveID, Give] = {oneGive.Id: oneGive, towGive.Id: towGive, threeGive.Id: threeGive}


    def getGiveByID(self: FakeRepository, giveID: GiveID) -> Optional[Give]:
        return self.DB.get(giveID)
    
    def saveGive(self: FakeRepository, give: Give) -> Optional[Give]:
        self.DB[give.Id] = give

        return self.getGiveByID(give.Id)   
    
fake_repository: FakeRepository = FakeRepository()

def test_get_give() -> None:
    _Give: Give = Give(Id=333, Amount=600, Date=datetime.now())
    newGive: Give = fake_repository.getGiveByID(giveID=_Give.Id)

    assert newGive.Id == _Give.Id
    assert newGive.Amount == _Give.Amount

def save_and_check() -> None:
    _Give: Give = Give(Id=444, Amount=700, Date=datetime.now())
    fake_repository.saveGive(give=_Give)

    newGive: Give = fake_repository.getGiveByID(giveID=_Give.Id)

    assert newGive.Id == _Give.Id
    assert newGive.Amount == _Give.Amount