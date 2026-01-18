from typing import Optional
from types import TracebackType

class GlobalUOW():
    def __init__(self: GlobalUOW) -> GlobalUOW:
        self.errors: list[str] = []

    def __enter__(self: GlobalUOW) -> GlobalUOW:
        return self
    
    def __exit__(self: GlobalUOW, exc_type: type[BaseException], exc_value: Optional[BaseException], traceback: TracebackType) -> None:
        if not exc_type is None:
            if not exc_value in self.errors:
                self.errors.append(exc_value)

            print(f"\n\nОшибка программы: {exc_value}")
