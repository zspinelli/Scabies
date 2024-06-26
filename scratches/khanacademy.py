# scabies.
from scabies import args_output, Strings
from scabies.scraper import Scraper


class KhanAcademy(Scraper):
    def __init__(self):
        super().__init__("khanacademy", "https://www.khanacademy.org")


    def _parse_args(self, args: list):
        pass


    def run(self, args: list):
        pass


def run(args: list):
    scraper: KhanAcademy = KhanAcademy()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
