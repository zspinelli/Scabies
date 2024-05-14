# scabies.
from scabies.scraper import Scraper

# scraping.


NAME: str = "reddit"
DOMAIN: str = ""


class Reddit(Scraper):
    def __init__(self):
        super().__init__(NAME)