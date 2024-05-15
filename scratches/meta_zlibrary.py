# scabies.
from scabies import Strings
from scabies.scraper import Scraper

# stdlib.
import itertools, string
from argparse import ArgumentParser
from multiprocessing import cpu_count ,Pool
from os import path

# scraping.
from bs4 import BeautifulSoup
from requests import Response


NAME: str = "zlibrary"
DOMAIN: str = "https://singlelogin.re"


class ZLibraryMeta(Scraper):
    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

        self._parse_args(args)

        thread_pool: Pool = Pool(cpu_count())

        group: str = "0" * 7

        while group != "z" * 7:
            thread_pool.apply_async(self._async_task, group)

            group = self._increment_ordinator_string(group)

        print(Strings.OP_FINISHED.format(NAME))


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for zlibrary")

        parser.add_argument(
            "-o",
            help="output path. writes scrape result log in the given directory.",
            dest="output"
        )

        parser.add_argument(
            '-ls',
            default="1024mb",
            type=self._parse_log_size,
            help="log size. restrict the result logs filesize. units: (b, kb, mb, gb)",
            dest="log_size"
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")


    def _parse_log_size(self, arg: str):
        # todo: finish.
        pass


    def _async_task(self, group: str):
        result_log = None
        hash: str = "0" * 6

        while hash != "z" * 6:
            group_hash: str = f"{group}/{hash}"

            print(f"testing: {group_hash} ... ", end="")

            probe_url: str = f"{DOMAIN}/book/{group_hash}"
            probe_response: Response = self._sess.get(probe_url)

            page_soup: BeautifulSoup = BeautifulSoup(probe_response.text, "html.parser")
            book_page = page_soup.find("body", {"class": "books/details"})

            # found a book page.
            if book_page:
                print("found book page.")

                # log not open yet.
                if not result_log:
                    result_log = open(path.join(self._args.output, "results.txt"), "w+")

                result_log.write(f"{group_hash}\n")

            # got redirected to home.
            else:
                print("nothing here.")

            hash = self._increment_ordinator_string(hash)


    def _increment_ordinator_string(self, ord_string: str) -> str:
        # saftey mechanism.
        if not ord_string:
            return ""

        i: int = -1

        while True:
            ord_val: int = ord(ord_string[i])

            # rollover from '9' to 'a'.
            if ord_val == 57:
                ord_string = ord_string[:i] + "a" + ord_string[i:]
                break

            # increment 0-9, or a-z.
            elif ord_val < 57 or ord_val < 122:
                ord_string = ord_string[:i] + chr(ord_val + 1) + ord_string[i:]
                break

            # rollover from 'z' to '0'.
            elif ord_val == 122:
                ord_string = ord_string[:i] + "0" + ord_string[i:]
                i += 1

        return ord_string


def run(args: list):
    scraper: ZLibraryMeta = ZLibraryMeta()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
