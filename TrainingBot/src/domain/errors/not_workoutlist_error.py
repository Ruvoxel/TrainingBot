class WorkoutListError(Exception):
    def __init__(self):
        self.server: bool = True
        super().__init__("Не было найдено ни одной тренеровочной недели!")