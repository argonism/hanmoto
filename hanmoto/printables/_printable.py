import abc
from typing import Dict, Union

PROPERTIES_TYPE = Dict[str, Union[bool, int, str]]


class Printable(metaclass=abc.ABCMeta):
    """
    Abstract base class for printable objects that can be passed to Hanmoto.
    """

    ...
