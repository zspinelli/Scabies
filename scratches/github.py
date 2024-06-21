# scabies.
from scabies.scraper import Scraper


class Github(Scraper):
    def __init__(self):
        super().__init__("github", "https://www.github.com")
