class notTypeFoundError(Exception):
    def __init__(self, *args):
        self.server: bool = True
        super().__init__("Тип/Обьект не был найден.")
   