class HmtException(Exception):
    """
    Hanmoto Base Exception.
    """

    def __init__(self, msg: str) -> None:
        self.message = msg
        super().__init__(self.message)


class HmtValueException(HmtException):
    """
    Hanmoto Value Exception.
    """


class HmtDuplicateInitializeException(HmtException):
    """
    Hanmoto Duplicaited Initialization Exception.
    """


class HmtWebAPIException(HmtException):
    """
    Hanmoto WebApi Exception.
    """


class HmtWebAPISequenceException(HmtWebAPIException):
    """
    Hanmoto API Sequence Print Exception.
    """
