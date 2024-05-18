# scabies.
from scabies import session, Strings
from scratches.neo_generic import Generic

# stdlib.
from os import makedirs, path
from urllib.parse import ParseResult, urlparse

# scraping.
from bs4 import BeautifulSoup, ResultSet
from requests import Response


NAME: str = "military-factory"
DOMAIN: str = "www.militaryfactory.com"


class MilitaryFactory(Generic):
    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        print(strings.OP_STARTING.format(self.name()))

        self._sess = session.new()
        self._parse_args(args)

        for url in self._args.urls:
            self._url_parts: ParseResult = urlparse(url)
            print(self._url_parts)

            urls_done: list = []
            urls_todo: list = []

            page_response: Response = self._sess.get(url)
            page_soup: BeautifulSoup = BeautifulSoup(page_response.text, "html.parser")

            self._destination_dir = f"{self._args.o}/{self._url_parts.netloc}{path.splitext(self._url_parts.path)[0]}"
            #print(self._destination_dir)

            makedirs(self._destination_dir, exist_ok=True)
            self._html_file = open(f"{self._destination_dir}{self._url_parts.query}", "a")

            anchors: ResultSet = page_soup.find_all("a", href=True)
            self._scrape_anchors(anchors)

            scripts: ResultSet = page_soup.find_all("script")
            self._scrape_scripts(scripts)

            images: ResultSet = page_soup.find_all("img")
            self._scrape_images(images)

            links: ResultSet = page_soup.find_all("link")
            urls_todo.append(self._scrape_links(links))

            urls_done.append(url)
            self._html_file.close()

        print(strings.OP_FINISHED.format(self.name()))


def run(args: list):
    scraper: MilitaryFactory = MilitaryFactory()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
