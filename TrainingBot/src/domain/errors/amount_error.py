class AmountError(Exception):
    def __init__(self: AmountError):
        self.server: bool = True
        super().__init__("Сумма должна быть положительным числом.")