# stdlib.
from argparse import ArgumentParser

# scabies.
from scabies.scraper import Scraper


class Flikr(Scraper):
    _flikr_api_key: str = ""
    _flikr_api_secret: str = ""

    # "db379ffce702100dbd2ffc9087eabaf5"
    # "e21a214e90596cf5"

    def __init__(self):
        super().__init__("flikr", "https://www.flikr.com")


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser()
        modes = parser.add_subparsers()


    def run(self, args: list):
        pass


def run(args: list):
    scraper: Scraper = Scraper()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
