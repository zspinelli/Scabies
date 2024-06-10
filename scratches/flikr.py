# scabies.
from scabies.scraper import Scraper


class Flikr(Scraper):
    def __init__(self):
        pass


def run(args: list):
    scraper: Scraper = Scraper()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
