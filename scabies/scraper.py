# stdlib.
from argparse import Namespace
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from multiprocessing import cpu_count
from os import path
from urllib.parse import urlparse, ParseResult

# scraping.
from bs4 import BeautifulSoup
from requests import Response

# scabies.
from scabies import session, Strings
from scabies.session import ScabiesSession


class ScraperInfo:
    def __init__(self, name: str, domain: str, modes: list, particles: dict):
        self.NAME = name
        self.DOMAIN = domain
        self.MODE = None

        # ---- modes. ---- #

        for mode in modes:
            setattr(self.MODE, mode.upper(), mode.lower())

        # ---- parts. ---- #

        for key, value in particles:
            default: list = []
            legend: list = []

            setattr(self, key.upper(), None)
            attr = getattr(self, key.upper())

            for name, code in value:
                pass

            setattr(attr, "LEGEND", default)
            setattr(attr, "DEFAULT", legend)


class Scraper:
    __doc__ = "base class for all scrapers. features name(), run(), and _parse_args() to " \
        "assist automation by the umbrella cli."

    def __init__(
        self,
        name: str = "generic",
        domain: str = "",
        interval: int = 0
    ):
        self._name: str = name
        self._domain: str = domain
        self._args: Namespace = Namespace()
        self._sess: ScabiesSession = session.new(interval)
        self._destination_dir: str = ""
        self._resume_filepath: str = ""
        self._resume_time: datetime = datetime.min


    def name(self) -> str:
        return self._name

    name.__doc__ = "return the name of the scraper as str"


    def domain(self) -> str:
        return self._domain

    domain.__doc__ = "return the domain of the scraper as str"


    def _parse_args(self, args: list):
        args = args[1:]

        parsed: Namespace = Namespace()

        # found help.
        if "-h" in args or "--help" in args:
            print(
                "usage: scraper.py [-h] [-o OUTPUT_STRUCTURED] [urls URL1 URL2 ...]\n\n"
                "positional arguments:\n"
                "  urls\t\tspace-separated sequence of art urls\n\n"
                "options:\n"
                "  -h, --help\t\tshow this help message and exit"
            )

        # found output.
        elif args.pop(0) == "-o":
            setattr(parsed, "output", args.pop(0))
            setattr(parsed, "urls", args)

        self._args = parsed
        print(f"input: {self._args}")

    _parse_args.__doc__ = "parse the parameters: list[str] passed from self.run()"


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

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

        print(Strings.OP_FINISHED.format(self.name()))

    run.__doc__ = "run the scraper on parameters: list[str] passed to args"


class MetaScraper(Scraper):
    def __init__(self, name, domain, thread_task, print_stats):
        super().__init__(name, domain)

        self._sess = None

        self._slots: list = []
        self._num_slots: int = cpu_count() * 2
        self._pool: ProcessPoolExecutor = ProcessPoolExecutor(self._num_slots)

        self._thread_task = thread_task
        self._print_stats = print_stats


    def _main_task(self):
        # ---- initialize slots. ---- #

        for i in range(self._num_slots):
            pass

        # ---- process. ---- #

        for slot in self._slots:
            self._pool.submit(self._thread_task, slot)






        for i in range(cpu_count()):
            self._slots.append(_Slot(self._next_uname))
            self._next_group = self._increment_ordinator_string(self._next_group)

        # ---- resume previous operation. ---- #

        # need to resume previous operation.
        if self._args.need_state_resume and path.isfile(self._resume_filepath):
            resume_file = open(self._resume_filepath, "r")
            i: int = 0

            for line in resume_file.readlines():
                self._slots[i].name = line
                i += 1

            resume_file.close()



def run(args: list):
    scraper: Scraper = Scraper()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
