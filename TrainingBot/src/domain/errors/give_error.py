class GiveError(Exception):
    def __init__(self):
        self.server: bool = True
        super().__init__("Не найдено ни одного подарка.")