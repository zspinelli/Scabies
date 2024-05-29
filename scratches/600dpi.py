# scabies.
from scabies import args_output, Strings, args_time
from scabies.scraper import Scraper

# stdlib.
import re
from argparse import ArgumentParser, REMAINDER

# scraping.
from bs4 import BeautifulSoup, ResultSet
from requests import Response


class SixHundredDPI(Scraper):
    class MODES:
        SEARCH: str = "search"
        ART: str = "art"


    def __init__(self):
        super().__init__("600dpi", "https://en.publicdomainr.net")


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description=f"scabies for {self._name}")
        modes = parser.add_subparsers(
            title="modes",
            dest="mode",
            required=True,
            help="see individual mode helps for additional options"
        )

        # ---- external features. ---- #

        args_output.add_output_args(parser)
        args_output.add_metadata_args(parser)

        # ---- search mode. ---- #

        search_mode: ArgumentParser = modes.add_parser(self.MODES.SEARCH)

        args_time.add_time_selection_args(search_mode)

        search_mode.add_argument(
            "terms",
            nargs=REMAINDER,
            help=Strings.SEQ_SEP_SPACE.format("search terms")
        )

        # ---- art mode. ---- #

        art_mode: ArgumentParser = modes.add_parser(self.MODES.ART)

        art_mode.add_argument(
            "urls",
            nargs=REMAINDER,
            help=Strings.SEQ_SEP_SPACE.format("art urls")
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.ou:
            self._destination_dir = self._args.ou

        args_output.validate_metadata_args(self._args)

        args_time.validate_time_selection_args(self._args)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self._name))

        self._parse_args(args)

        # delegate to required mode.
        if self._args.mode == self.MODES.SEARCH:    self._process_search_mode()
        elif self._args.mode == self.MODES.ART:     self._process_art_mode()

        print(Strings.OP_FINISHED.format(self._name))





    def _process_art_mode(self):
        for url in self._args.urls:
            print("started art: " + url)

            print("finished art: " + url)


    def _process_search_mode(self):
        print(Strings.SEARCH_STARTED.format(""))

        for url in self._args.urls:
            page: int = 1

            while True:
                # page path already in url.
                if "/page/" in url:
                    url = re.sub(r"/page/\d+/", f"/page/{page}/", url)

                # page path needs added.
                else:
                    parts: list = url.split('/')
                    url = '/'.join(parts[:3] + ["page/0"] + parts[3:])

                results_response: Response = self._sess.get(url)
                results_soup: BeautifulSoup = BeautifulSoup(results_response.text, "html.parser")

                scroll_wrapper = results_soup.find("div", id_="scroll-wrapper")
                results: ResultSet = scroll_wrapper.find_all("div")

                # no more pages.
                if not results_soup.find("a", class_="next page_numbers"):
                    break

            print(Strings.SEARCH_FINISHED.format(""))


    def _scrape_art(self, page_url: str):
        page_response: Response = self._sess.get(page_url)

        page_soup: BeautifulSoup = BeautifulSoup(page_response.text, "html.parser")

        art_link = page_soup.find("a", href=True)


def run(args: list):
    scraper: SixHundredDPI = SixHundredDPI()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
