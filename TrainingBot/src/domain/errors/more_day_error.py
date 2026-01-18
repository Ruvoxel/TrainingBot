class moreDayError(Exception):
    def __init__(self):
        self.server: bool = True
        super().__init__("Тренировочных дней не должно привышать 7 дней.")