class UsernameError(Exception):
    def __init__(self: UsernameError):
        self.server: bool = True
        super().__init__("Невалидное имя.")