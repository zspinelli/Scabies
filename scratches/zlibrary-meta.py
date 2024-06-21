# scabies.
from scabies import Strings
from scabies.scraper import Scraper

# stdlib.
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from os import path, makedirs

# scraping.
from blessed import Terminal
from bs4 import BeautifulSoup
from requests import Response


class _Slot:
    def __init__(self, group: str, code: str):
        self.group = group
        self.code = code


class ZLibraryMeta(Scraper):
    def __init__(self):
        super().__init__("zlibrary-meta", "https://z-library.rs/")

        self._MAX_GROUP_LENGTH: int = 9
        self._CODE_LENGTH: int = 6

        self._aborted: bool = False
        self._slots: list = [_Slot("0" * 6, "0" * self._CODE_LENGTH)]


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description=f"scabies for {self._name}")

        parser.add_argument(
            "-o",
            required=True,
            help="output path. writes scrape result logs in the given directory.",
            dest="output"
        )

        parser.add_argument(
            "--lsr",
            action="store_true",
            help="load or save progress in log files",
            dest="need_state_resume"
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        print(f"input: {self._args}")


    def run(self, args: list):
        terminal = Terminal()
        pool: ThreadPoolExecutor = ThreadPoolExecutor()

        print(Strings.OP_STARTING.format(self._name))

        self._parse_args(args)

        # ---- resume previous operation. ---- #

        self._resume_filepath: str = f"{self._args.output}/{self._name}_resume.txt"

        # need to resume previous operation.
        if self._args.need_state_resume and path.isfile(self._resume_filepath):
            with open(self._resume_filepath, "r") as resume_file:
                line: str = resume_file.readline()
                parts: list = line.split(":")

                self._slots[0].group = parts[0]
                self._slots[0].code = parts[1]

        # ---- start mining. ---- #

        print("type \"q\" to stop:")
        pool.submit(self._task, self._slots[0])

        while self._slots:
            # user requests early exit.
            if input() in ["q", "Q"]:
                self._aborted = True
                break

        # need to store current operation.
        if self._args.need_state_resume :
            with open(self._resume_filepath, "w") as resume_file:
                resume_file.write(f"{self._slots[0].group}:{self._slots[0].code}")

        print(Strings.OP_FINISHED.format(self._name))


    def _task(self, slot: _Slot):
        result_log = None

        while(
            not self._aborted and
            slot.code != "z" * self._CODE_LENGTH
        ):
            group_hash: str = f"{slot.group}/{slot.code}"
            print(f"testing: {group_hash} ... ", end="")

            probe_url: str = f"{self._domain}/book/{group_hash}"
            probe_response: Response = self._sess.get(probe_url)

            page_soup: BeautifulSoup = BeautifulSoup(probe_response.text, "html.parser")
            book_page = page_soup.find("body", {"class": "books/details"})

            # found a book page.
            if book_page:
                print("found book page.")

                # log not open yet.
                if not result_log:
                    makedirs(self._args.output, exist_ok=True)
                    result_log = open(f"{self._args.output}/{self._name}_results.txt", "w+")

                result_log.write(f"{group_hash}\n")

            # found nothing.
            else:
                print()

            slot.code = self._increment_ordinator_string(slot.code)

        del slot


    def _increment_ordinator_string(self, ord_string: str) -> str:
        i: int = len(ord_string)

        while True:
            front: str = ord_string[:i - 1]
            back: str = ord_string[i:]
            ord_val: int = ord(ord_string[i - 1])

            # rollover everything and increase length.
            if all(char == 'z' for char in ord_string):
                ord_string = '0' * (len(ord_string) + 1)
                break

            # rollover from '9' to 'a'.
            if ord_val == 57:
                ord_string = front + "a" + back
                break

            # rollover from 'z' to '0'.
            elif ord_val == 122:
                ord_string = front + "0" + back
                i -= 1

            # increment 0-9, or a-z.
            elif ord_val < 57 or ord_val < 122:
                ord_string = front + chr(ord_val + 1) + back
                break

        return ord_string


def run(args: list):
    scraper: ZLibraryMeta = ZLibraryMeta()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
