class TotalCaloriesError(Exception):
    def __init__(self):
        self.server: bool = True
        super().__init__("Суммарная калории не должны быть отрицательными!")