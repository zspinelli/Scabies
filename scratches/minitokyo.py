# stdlib.
from argparse import ArgumentParser

# scabies.
from scabies.scraper import Scraper


class MiniTokyo(Scraper):
    def __init__(self):
        super().__init__("minitokyo", "http://www.minitokyo.net")


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for minitokyo")
        modes = parser.add_subparsers(
            title="modes",
            dest="mode",
            required=True,
            help="see individual mode helps for additional options"
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")


    def run(self, args: list):
        pass


def run(args: list):
    scraper: MiniTokyo = MiniTokyo()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
