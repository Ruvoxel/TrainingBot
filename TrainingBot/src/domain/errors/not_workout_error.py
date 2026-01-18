class NotWorkoutError(Exception):
    def __init__(self: NotWorkoutError):
        self.server: bool = True
        super().__init__("Не найдено тренажерных дней.")