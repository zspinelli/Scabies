# scabies.
from scabies.scraper import Scraper


NAME: str = "deviantart_meta"
DOMAIN: str = "https://www.deviantart.com/"


class MetaDeviantArt(Scraper):
    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        pass


    def _parse_args(self, args: list):
        pass
