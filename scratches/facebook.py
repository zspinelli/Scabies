# scabies.
from scabies.scraper import Scraper


class Facebook(Scraper):
    def __init__(self):
        super().__init__("facebook", "https://www.facebook.com")


    def _parse_args(self, args: list):
        pass


    def run(self, args: list):
        pass


def run(args: list):
    scraper: Facebook = Facebook()
    scraper.run(args)


# entry point.
if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
