from collections import Counter

from models.common import InputResults, InputResult, Input
from models.constants import InputType


def _validate_input(user_input: str, words: list[str]) -> bool:
    """
    Validates the user input string according to specific format rules.

    Parameters
    ----------
    user_input : str
        The input string to validate

    Returns
    -------
    bool
        True if the input is valid; otherwise False

    Notes
    -----
    The input is considered valid if:
    - It's not empty
    - Has matching brackets [] and ()
    - Brackets should enclose single characters
    - Contains exactly 5 unique characters (excluding brackets)
    """
    try:
        if not user_input:
            return False

        counter: Counter[str] = Counter(user_input)

        if (
                (counter.get("[") and counter.get("[") != counter.get("]"))
                or (counter.get("(") and counter.get("(") != counter.get(")"))
        ):
            return False

        for index in range(len(user_input)):
            if (
                    (user_input[index] == "[" and user_input[index + 2] != "]")
                    or (user_input[index] == "(" and user_input[index + 2] != ")")
            ):
                return False

        cleaned_word = [char.upper() for char in user_input if char not in["[", "]", "(", ")"]]
        if len(cleaned_word) != 5:
            return False

        if "".join(cleaned_word) not in words:
            return False

        return True
    except IndexError:
        return False


def _process_input(user_input: str) -> InputResults:
    """
    Processes the validated input string and converts it to InputResults.

    Parameters
    ----------
    user_input : str
        The validated input string to process

    Returns
    -------
    InputResults
        Collection of InputResult objects representing the processed input
    """
    
    results: InputResults = InputResults()
    index: int = 0
    while index != len(user_input):
        char: str = user_input[index]
        if char == "[":
            result: InputResult = InputResult.is_fixed(user_input[index + 1])
            results.push(result)
            index += 3
        elif char == "(":
            result: InputResult = InputResult.exists(user_input[index + 1])
            results.push(result)
            index += 3
        else:
            result: InputResult = InputResult.does_not_exist(char)
            results.push(result)
            index += 1

    return results

def get_input(words: list[str]) -> Input:
    """
    Retrieve and process user input through a validation loop.

    Returns
    -------
    InputResults
        The processed result of the valid user input
    """

    stripped_input: str = ""

    input_not_valid: bool = True
    while input_not_valid:
        user_input = input("> ")
        stripped_input = user_input.strip().upper()
        match stripped_input:
            case "GG":
                return Input(InputType.RESET, None)
            case "Q":
                return Input(InputType.EXIT, None)

        if _validate_input(stripped_input, words):
            input_not_valid = False
        else:
            print("Invalid input. Please try again.")
            
    processed_input: InputResults = _process_input(stripped_input)
    return Input(InputType.PROMPT, processed_input)

def ask_continue() -> bool:
    print("Game Over!")
    again = input("Do you want to play again? (y/n): ")
    return again.lower() == "y"