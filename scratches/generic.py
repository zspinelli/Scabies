# stdlib.
from argparse import ArgumentParser
from os import path
from urllib.parse import urlparse, ParseResult

# scraping.
from bs4 import BeautifulSoup
from requests import Response

# scabies.
from scabies import Strings
from scabies.scraper import Scraper


class Generic(Scraper):
    def __init__(self):
        super().__init__("generic", "*")


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser()

        parser.add_argument(
            "--ll",
            action="store_true",
            help="localize links. convert links in saved pages to refer to other saved pages",
            dest="localize_links"
        )

        parser.add_argument(
            "--id",
            action="store_true",
            help="ignore downloads. dont download zip, pdf, or other files from links in pages",
            dest="ignore_downloads"
        )

        parser.add_argument(
            "-o",
            help="output directory",
            dest="output"
        )

        parser.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("urls to scrape")
        )

        self._args = parser.parse_args()
        print(f"input: ", self._args)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self._name))

        self._parse_args(args)

        for url in self._args.urls:
            url_parts: ParseResult = urlparse(url)

            origin_domain: str = url_parts.netloc

            urls_todo: list = [url]
            urls_done: list = []

            while urls_todo:
                current_url = urls_todo.pop(0)

                page_response: Response = self._sess.get(current_url)
                page_soup: BeautifulSoup = BeautifulSoup(page_response.text, "html.parser")

                # ---- ensure destination. ---- #

                _url_parts: ParseResult = urlparse(current_url)
                #print("url_parts:", _url_parts)

                page_name: str = path.basename(_url_parts.path)
                page_path: str = path.dirname(_url_parts.path)
                path.join(self._args.output, _url_parts.netloc, page_path, page_name, ".html")

                #self._destination_dir = f"{self._args.output}/{self._url_parts.netloc}{path.splitext(self._url_parts.path)[0]}"
                # print(self._destination_dir)

                #makedirs(self._destination_dir, exist_ok=True)
                #self._html_file = open(f"{self._destination_dir}{self._url_parts.query}", "w")

                """
                # ---- scrape resources. ---- #

                anchors: ResultSet = page_soup.find_all("a", href=True)
                # self._scrape_anchors(anchors)

                for anchor in anchors:
                    print(anchor)

                scripts: ResultSet = page_soup.find_all("script")
                # self._scrape_scripts(scripts)

                images: ResultSet = page_soup.find_all("img")
                # self._scrape_images(images)

                for image in images:
                    print(images)

                links: ResultSet = page_soup.find_all("link")
                # urls_todo.append(self._scrape_links(links))

                for link in links:
                    print(link)
                """

                # ---- prepare for next url. ---- #

                urls_done.append(current_url)
                #self._html_file.close()

        print(Strings.OP_FINISHED.format(self._name))


    def _url_on_same_domain(self) -> bool:
        return False


def run(args: list):
    scraper: Generic = Generic()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
