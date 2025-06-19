from models.common import InputResults

class SuggestionService:
    """A service class for managing word suggestions based on input results."""

    def __init__(self, words: list[str]) -> None:
        """
        Initialize the SuggestionService with a list of valid words.

        Parameters
        ----------
        words : list[str]
            List of valid words to use for suggestions
        """

        self._words: set[str] = set(words)
        self._filtered_words: set[str] = set()
        self._fixed: list[str | None] = [None, None, None, None, None]
        self._exists_but_not_here: list[set[str]] = [set(),set(),set(),set(),set()]
        self._does_not_exist: set[str] = set()

    def _process_inputs(self, inputs: InputResults) -> None:
        """
        Process the input results and update internal character tracking lists.

        Parameters
        ----------
        inputs : InputResults
            Collection of input results containing character validations
        """

        for index, char in enumerate(inputs):
            if char.is_fixed:
                self._fixed[index] = char.char
            elif char.exists_but_not_here:
                self._exists_but_not_here[index].add(char.char)
            else:
                self._does_not_exist.add(char.char)

    def get_suggestion(self, inputs: InputResults) -> list[str]:
        """
        Generate a word suggestion based on the provided input results.

        Parameters
        ----------
        inputs : InputResults
            Collection of input results containing character validations

        Returns
        -------
        str
            A suggested word based on the input results
        """

        self._process_inputs(inputs)

        required_chars: set[str] = {char for char in {*self._fixed}.union({char for position in self._exists_but_not_here for char in position}) if char}

        def suggestion_filter(word: str) -> bool:
            """
            Filter words based on character position rules and requirements.

            Parameters
            ----------
            word : str
                The word to be evaluated against the filtering rules

            Returns
            -------
            bool
                True if the word matches all filtering criteria;  otherwise False

            Notes
            -----
            The word is filtered based on:
            - Required characters that must be present
            - Characters that must not exist in the word
            - Characters that must be in specific positions
            - Characters that exist but cannot be in specific positions
            """

            striped_word: str = word.strip()
            word_set: set[str] = set(striped_word)
            if (
                    (required_chars and not required_chars.issubset(word_set))
                    or (self._does_not_exist and (self._does_not_exist & word_set))
            ):
                return False

            for index, char in enumerate(striped_word):
                if (
                        (self._fixed[index] and self._fixed[index] != char)
                        or (self._exists_but_not_here[index] and char in self._exists_but_not_here[index])
                ):
                    return False

            return True

        self._filtered_words = set(filter(suggestion_filter, self._filtered_words or self._words))
        return list(self._filtered_words)[:5]


    def reset(self):
        """
        Reset all internal character lists to their initial empty state.
        """

        self._filtered_words = set()
        self._fixed = [None, None, None, None, None]
        self._exists_but_not_here = [set(),set(),set(),set(),set()]
        self._does_not_exist = set()