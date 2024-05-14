# stdlib.
from abc import ABC, abstractmethod
from argparse import Namespace
from datetime import datetime

# scraping.
from requests import Session

# scabies.
from scabies import session


class Resolver(ABC):
    __doc__ = "utility for the umbrella cli to resolve how to automate detected scrapers."

    def __init__(self, patterns: str):
        pass


    def match(self, string: str):
        pass

    match.__doc__ = "try to match the string with one of the patterns."




class Scraper(ABC):
    __doc__ = "base class for all scrapers. features name(), run(), and _parse_args() to " \
        "assist automation by the umbrella cli."

    def __init__(self, name: str, interval: int = 0):
        self._name: str = name
        self._args: Namespace = Namespace()
        self._sess: Session = session.new(interval)
        self._destination_dir: str = ""
        self._resume_filepath: str = ""
        self._resume_time: datetime = datetime.min


    def name(self) -> str:
        return self._name

    name.__doc__ = "return the name of the scraper as str"


    @abstractmethod
    def run(self, args: list):
        pass

    run.__doc__ = "run the scraper on parameters: list[str] passed to args"


    @abstractmethod
    def _parse_args(self, args: list):
        pass

    _parse_args.__doc__ = "parse the parameters: list[str] passed from self.run()"
