from dataclasses import dataclass
from typing import Iterable, Iterator, NamedTuple

from models.constants import InputType


class Input(NamedTuple):
    type: InputType
    result: "InputResults"

@dataclass
class InputResults(Iterable):
    """
    Represents a collection of input results.

    This class is used to maintain a list of input results. It provides functionality
    to add new input results to the collection and manage them as a group.

    """

    def __init__(self):
        self._results: list[InputResult] = []

    def __getitem__(self, index) -> "InputResult":
        return self._results[index]

    def __iter__(self) -> "Iterator[InputResult]":
        return iter(self._results)

    def push(self, input_result: "InputResult") -> None:
        self._results.append(input_result)

@dataclass
class InputResult:
    """
    A class representing the result of character input validation.

    Attributes
    ----------
    char : str
        The character being validated
    is_fixed : bool
        Whether the character position is fixed
    exists_but_not_here : bool
        Whether the character exists in the target word, but not on this position
    """

    def __init__(self, char: str, is_fixed: bool, exists_but_not_here: bool):
        self.char = char
        self.is_fixed = is_fixed
        self.exists_but_not_here = exists_but_not_here

    @staticmethod
    def does_not_exist(char: str) -> "InputResult":
        return InputResult(char=char, is_fixed=False, exists_but_not_here=False)

    @staticmethod
    def is_fixed(char: str) -> "InputResult":
        return InputResult(char=char, is_fixed=True, exists_but_not_here=False)

    @staticmethod
    def exists(char: str) -> "InputResult":
        return InputResult(char=char, is_fixed=False, exists_but_not_here=True)