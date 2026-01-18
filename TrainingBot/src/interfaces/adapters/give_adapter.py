from typing import Optional, Final

from ..ports import portGiveRepository
from ...domain import Give, GiveID

class adapterGiveRepository(portGiveRepository):
    def __init__(self: adapterGiveRepository) -> adapterGiveRepository:
        self.DB: list[dict[GiveID, Give]] = [{}]

    def getGiveByID(self: adapterGiveRepository, giveID: GiveID) -> Optional[list[Give]]:
        filters: list[dict[GiveID, Give]] = list(filter(lambda give: list(give.keys())[0] == giveID if give != {} else False, self.DB))
        return list(map(lambda item: item.get(giveID), filters))
        
    
    def saveGive(self: adapterGiveRepository, give: Give) -> Optional[Give]:
        Id: Final[GiveID] = give.Id
        try:
            Index: int = self.DB.index({Id: give})
            self.DB[Index][Id] = give
        except ValueError:
            self.DB.append({Id: give})

        return self.getGiveByID(give.Id)