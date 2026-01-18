class ResponseError(Exception):
    def __init__(self):
        self.server: bool = True
        super().__init__("Неверный формат для ответа.")