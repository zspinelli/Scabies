# stdlib.

# scabies.
from scabies.scraper import Scraper


NAME: str = "minitokyo"
DOMAIN: str = "http://www.minitokyo.net/"


class MiniTokyo(Scraper):
    def __init__(self):
        super().__init__(NAME)