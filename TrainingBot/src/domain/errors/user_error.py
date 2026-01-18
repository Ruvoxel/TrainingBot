class UserError(Exception):
    def __init__(self):
        self.server: bool = True
        super().__init__("Пользователь уже есть, добавить второго с таким же ID невозможно/Техническая ошибка.")