class TexError(Exception):
    def __init__(self):
        self.server: bool = True
        super().__init__("Техническая ошибка сервера.")