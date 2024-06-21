# scabies.
from scabies.scraper import Scraper


class SciHubMeta(Scraper):
    def __init__(self):
        super().__init__("scihub-meta", "")
