# stdlib.
from abc import ABC
from argparse import Namespace, ArgumentParser, REMAINDER
from datetime import datetime
from os import path, makedirs
from urllib.parse import urlparse, ParseResult

# scraping.
from bs4 import ResultSet, BeautifulSoup
from requests import Session, Response

# scabies.
from scabies import session, Strings


NAME: str = "generic"
DOMAIN: str = "*"


class Resolver(ABC):
    __doc__ = "utility for the umbrella cli to resolve how to automate detected scrapers."

    def __init__(self, patterns: str):
        pass


    def match(self, string: str):
        pass

    match.__doc__ = "try to match the string with one of the patterns."


class Scraper:
    __doc__ = "base class for all scrapers. features name(), run(), and _parse_args() to " \
        "assist automation by the umbrella cli."


    def __init__(self, name: str, interval: int = 0):
        self._name: str = name
        self._args: Namespace = Namespace()
        self._sess: Session = session.new(interval)
        self._destination_dir: str = ""
        self._resume_filepath: str = ""
        self._resume_time: datetime = datetime.min


    def name(self) -> str:
        return self._name

    name.__doc__ = "return the name of the scraper as str"


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

        self._parse_args(args)

        urls_todo: list = self._args.urls
        urls_done: list = []

        print(Strings.OP_FINISHED.format(self.name()))

        """
        while urls_todo:
            current_url: str = urls_todo.pop()

            url_parts = urlparse(current_url)
            print(url_parts)

            #self._destination_dir =


            page_response: Response = self._sess.get(current_url)
            page_soup: BeautifulSoup = BeautifulSoup(page_response.text, "html.parser")

            # ---- ensure destination. ---- #

            self._url_parts: ParseResult = urlparse(current_url)
            print(self._url_parts)

            self._destination_dir = f"{self._args.o}/{self._url_parts.netloc}{path.splitext(self._url_parts.path)[0]}"
            #print(self._destination_dir)

            makedirs(self._destination_dir, exist_ok=True)
            self._html_file = open(f"{self._destination_dir}{self._url_parts.query}", "w")

            # ---- scrape resources. ---- #

            anchors: ResultSet = page_soup.find_all("a", href=True)
            #self._scrape_anchors(anchors)

            for anchor in anchors:
                print(anchor)

            scripts: ResultSet = page_soup.find_all("script")
            #self._scrape_scripts(scripts)

            images: ResultSet = page_soup.find_all("img")
            #self._scrape_images(images)

            for image in images:
                print(images)

            links: ResultSet = page_soup.find_all("link")
            #urls_todo.append(self._scrape_links(links))

            for link in links:
                print(link)

            # ---- prepare for next url. ---- #

            urls_done.append(current_url)
            self._html_file.close()
            
        """

    run.__doc__ = "run the scraper on parameters: list[str] passed to args"


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description=f"scabies for {NAME}")

        parser.add_argument(
            '-o',
            dest='output',
            type=str,
            help='Output file'
        )

        parser.add_argument(
            'urls',
            nargs=REMAINDER,
            type=str,
            help='URLs to scrape'
        )

        self._args = parser.parse_args(args)

    _parse_args.__doc__ = "parse the parameters: list[str] passed from self.run()"


def run(args: list):
    scraper: Scraper = Scraper(NAME)
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
