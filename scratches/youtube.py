# scabies.
from scabies.scraper import Scraper


class YouTube(Scraper):
    def __init__(self):

        super().__init__("youtube", "https://www.youtube.com")


    def _parse_args(self, args: list):
        pass


    def run(self, args: list):
        pass


def run(args: list):
    scraper: YouTube = YouTube()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
