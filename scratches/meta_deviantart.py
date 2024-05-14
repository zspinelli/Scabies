# scabies.
from scabies.scraper import Scraper


NAME: str = "deviantart_meta"
DOMAIN: str = ""


class MetaDeviantArt(Scraper):
    def __init__(self):
        super().__init__(NAME)
