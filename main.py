import os
import sys

from models.constants import InputType
from services.io_service import get_input, ask_continue
from services.suggestion_service import SuggestionService

ROOT_DIR: str = os.path.dirname(os.path.abspath(__file__))
FILE_NAME: str = "resources/words.txt"

def _initialize() -> list[str]:
    with open(os.path.join(ROOT_DIR, FILE_NAME), "r") as file:
        return file.read().splitlines()

def main() -> int:
    try:
        print("Welcome to Wordle Solver!")

        words: list[str] = _initialize()

        suggestion_serivce: SuggestionService = SuggestionService(words)

        exit: bool = False
        turns: int = 0

        while not exit:
            if turns == 6:
                should_continue: bool = ask_continue()
                if should_continue:
                    turns = 0
                    suggestion_serivce.reset()
                else:
                    exit = True
                    continue

            (input_type, prompt) = get_input(words)
            if input_type == InputType.EXIT:
                exit = True
                continue
            elif input_type == InputType.RESET:
                turns = 0
                suggestion_serivce.reset()
                print("New Wordle!")
                continue

            suggestions: list[str] = suggestion_serivce.get_suggestion(prompt)
            if not suggestions:
                should_continue: bool = ask_continue()
                if should_continue:
                    turns = 0
                    suggestion_serivce.reset()
                else:
                    exit = True
                    continue

            print([suggestion.strip() for suggestion in suggestions])
            turns += 1

        print("Thanks for playing!")
        return sys.exit(0)
    except Exception as e:
        print("An error occurred. Please try again.", str(e))
        return sys.exit(1)


if __name__ == "__main__":
    main()