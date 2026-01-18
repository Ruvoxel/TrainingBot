class notBonusError(Exception):
    def __init__(self):
        self.server: bool = True
        super().__init__("Вы уже получали бесплатную награду/Не выполнили ежедневную задачу.")