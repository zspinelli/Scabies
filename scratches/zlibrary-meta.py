"""
what im thinking about while working on the meta scrapers is
making a special base class for them to share their multithreading and tor routing implementation.
additionally i'd like to add a blessed tui to display stats about the scraping and threads at the same
time as offering a command prompt to pause or abort the scrape. a high speed scroll of hashes being tested
isnt' very informative.
"""


# scabies.
from scabies import Strings, session, tor
from scabies.scraper import Scraper

# stdlib.
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count, Lock
from os import path

# scraping.
from bs4 import BeautifulSoup
from requests import Response


class _Slot:
    def __init__(self, start_group: str, start_hash: str):
        self.group: str = start_group
        self.hash: str = start_hash


class ZLibraryMeta(Scraper):
    def __init__(self):
        super().__init__("zlibrary-meta-all-books", "https://singlelogin.re")

        self._sess = None

        self._MAX_GROUP_LENGTH: int = 7
        self._HASH_LENGTH: int = 6

        self._next_group: str = "0"
        self._next_group_lock: Lock = Lock()

        self._pool: ProcessPoolExecutor | None = None
        self._slots: list = []


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
        #print(f"input: {self._args}")


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

        self._parse_args(args)

        self._resume_filepath: str = f"{self._args.output}/{self._name}_resume.txt"

        with ProcessPoolExecutor(cpu_count() + 1) as self._pool:
            self._pool.submit(self._manage_slots_task)

            while True:
                # user requests early exit.
                if input("type \"q\" to stop:") in ["q", "Q"]:
                    break

        print(Strings.OP_FINISHED.format(self._name))


    def _manage_slots_task(self):
        # ---- initialize slots. ---- #

        for i in range(cpu_count()):
            self._slots.append(_Slot(self._next_group, "0"))
            self._next_group = self._increment_ordinator_string(self._next_group)

        # ---- resume previous operation. ---- #

        # need to resume previous operation.
        if self._args.need_state_resume and path.isfile(self._resume_filepath):
            resume_file = open(self._resume_filepath, "r")
            i: int = 0

            for line in resume_file.readlines():
                parts: list = line.split(":")

                self._slots[i].group = parts[0]
                self._slots[i].hash = parts[1]

                i += 1

            resume_file.close()

        # ---- process. ---- #

        for slot in self._slots:
            self._pool.submit(self._group_hashes_task, slot)


    def _group_hashes_task(self, slot: _Slot):
        sess = session.new(0)
        #tor.start()

        result_log = None

        while slot.hash != "z" * self._HASH_LENGTH:
            group_hash: str = f"{slot.group}/{slot.hash}"

            print(f"testing: {group_hash} ... ", end="")

            probe_url: str = f"{self._domain}/book/{group_hash}"
            probe_response: Response = sess.get(probe_url)

            page_soup: BeautifulSoup = BeautifulSoup(probe_response.text, "html.parser")
            book_page = page_soup.find("body", {"class": "books/details"})

            # found a book page.
            if book_page:
                print("found book page.")

                # log not open yet.
                if not result_log:
                    result_log = open(path.join(self._args.output, "results.txt"), "w+")

                result_log.write(f"{group_hash}\n")

            slot.hash = self._increment_ordinator_string(slot.hash)

        del slot


    def _increment_ordinator_string(self, ord_string: str) -> str:
        # saftey mechanism.
        if not ord_string:
            return ""

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