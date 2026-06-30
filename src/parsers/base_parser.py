from abc import ABC, abstractmethod
from typing import List, Union
from src.models.parsed_candidate import ParsedCandidate


class BaseParser(ABC):
    """
    Abstract base class for all parsers.

    Every parser in the system (CSV, Resume, GitHub, LinkedIn, etc.)
    must inherit from this class and implement the parse() method.
    """

    @abstractmethod
    def parse(self, source: str) -> Union[ParsedCandidate, List[ParsedCandidate]]:
        """
        Parse the given source and return one or more ParsedCandidate objects.

        Parameters
        ----------
        source : str
            Path, URL, or identifier of the input source.

        Returns
        -------
        ParsedCandidate | List[ParsedCandidate]
            Parsed candidate information extracted from the source.

        Raises
        ------
        NotImplementedError
            If the child class does not implement this method.
        """
        pass