from src.unit_of_work import GlobalUOW

def test_errors() -> None:
    unit_of_work: GlobalUOW = GlobalUOW()


    try:
        with unit_of_work:
            raise TypeError("TypeError")
    except TypeError:
        pass

    
    try:
        with unit_of_work:
            raise AttributeError("AttributeError")
    except AttributeError:
        pass


    try:
        with unit_of_work:
            raise ValueError("ValueError")
    except ValueError:
        pass


    assert len(unit_of_work.errors) == 3