# stdlib.

# scabies.
from scabies.scraper import Scraper


class MiniTokyo(Scraper):
    def __init__(self):
        super().__init__("minitokyo", "http://www.minitokyo.net")


    def _parse_args(self, args: list):
        pass


    def run(self, args: list):
        pass


def run(args: list):
    scraper: MiniTokyo = MiniTokyo()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
