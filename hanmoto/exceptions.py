class HmtException(Exception):
    """
    Hanmoto Base Exception.
    """

    ...


class HmtValueException(HmtException):
    """
    Hanmoto Value Exception.
    """

    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(self.message)
