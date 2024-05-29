# scabies.
from scabies import Strings
from scabies.scraper import Scraper

# stdlib.
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Lock, cpu_count
from os import path

# scraping.
from bs4 import BeautifulSoup
from requests import Response


class _Slot:
    def __init__(self, num: int, start_group: str, start_hash: str):
        self.num: int = num
        self.group: str = start_group
        self.next_group: str = ""
        self.hash: str = start_hash
        self.done: bool = False


class ZLibraryMeta(Scraper):
    _GROUP_LENGTH: int = 7
    _HASH_LENGTH: int = 6

    def __init__(self):
        super().__init__("zlibrary-meta", "https://singlelogin.re")

        self._next_group: str = "0" * 7
        self._next_group_lock: Lock = Lock()
        self._slots: list = []


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

        self._parse_args(args)

        # ---- initialize slots. ---- #

        for i in range(cpu_count()):
            self._slots.append(_Slot(i, self._next_group, "0" * 6))
            self._next_group = self._increment_ordinator_string(self._next_group)

        # need to resume previous operation.
        if self._args.need_state_resume:
            # todo: load savestate.
            pass

        # ---- process. ---- #

        with ProcessPoolExecutor() as pool:
            while True:
                for slot in self._slots:
                    pool.submit(self._group_hashes_task, slot)

                break

        print(Strings.OP_FINISHED.format(self._name))


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description=f"scabies for {self._name}")

        parser.add_argument(
            "-o",
            help="output path. writes scrape result logs in the given directory.",
            dest="output"
        )

        parser.add_argument(
            "--lsr",
            action="store_true",
            help="resume last run state from logs",
            dest="need_state_resume"
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")


    def _group_hashes_task(self, slot: _Slot):
        hash: str = start_hash

        while hash != "z" * 6:
            pass

        print("started testing group:", self._next_group)

        self._slots[]




    def _async_task(self, group: str, hash_slot: int, hash: str= "0" * 6):
        result_log = None


        while hash != "z" * 6:
            group_hash: str = f"{group}/{hash}"

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

        i: int = len(ord_string)

        while True:
            front: str = ord_string[:i - 1]
            back: str = ord_string[i:]
            ord_val: int = ord(ord_string[i - 1])

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
