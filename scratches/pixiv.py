# scabies.
from scabies.scraper import Scraper


NAME: str = "pixiv"
DOMAIN: str = "https://www.pixiv.net"


class Pixiv(Scraper):
    class MODES:
        SEARCH_URLS: str = "search"
        USER_IDS: str = "user"
        POST_IDS: str = "post"

    def __init__(self):
        super().__init__(NAME, DOMAIN)

        self._client_id: str = ""
        self._client_secret: str = ""




def resolve(url: str) -> list:
    pass


def run(args: list):
    scraper: Pixiv = Pixiv()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
