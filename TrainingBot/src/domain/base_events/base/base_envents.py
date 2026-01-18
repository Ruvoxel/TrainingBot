from typing import TypeVar, Type, Optional, Any
from functools import wraps
from types import TracebackType

Class = TypeVar('Class')

class BaseEnvents:
    def __init__(self, cls: Type[Class]) -> BaseEnvents:
        self.cls: Type[Class] = cls
        self.events: dict[object, callable] = {}

        setattr(self.cls, "Base", self)

    def __call__(self: BaseEnvents, *args, **kwds) -> Class:
        methods: dict = self.cls.__dict__
        for _, method in methods.items():
            try:
                if callable(method) and not method.__name__.startswith("__"):
                    method(self.cls)
                else:
                    continue
            except Exception:
                continue

        return self.cls(*args, **kwds)
    
    @staticmethod
    def setEnvent(event: object) -> callable:
        def decorator(func: callable) -> callable:
            @wraps(func)
            def wrapper(self: Type[Class]) -> None:
                self.Base.events[event] = func
            return wrapper
        return decorator

    def __enter__(self: Type[Class]) -> callable:
        def getEvent(event: object) -> Optional[Any]:
            method: callable = self.events.get(type(event))
            if method:
                return method(self)
        return getEvent
    
    def __exit__(self: BaseEnvents, exc_type: type[BaseException], exc_value: Optional[BaseException], traceback: TracebackType) -> None:
        pass