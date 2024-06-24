# scabies.
from scabies import Strings
from scabies.scraper import Scraper

# stdlib.
from argparse import ArgumentParser
from os import path, makedirs
from threading import Thread
from time import sleep

# scraping.
from requests import Response


class _Slot:
    def __init__(self, group, code):
        self.group: str = group
        self.code: str = code
        self.result: int = 0


class ZLibraryMeta(Scraper):
    def __init__(self):
        super().__init__("zlibrary-meta", "https://z-library.rs", timeout = 4)

        self._MAX_GROUP_LENGTH: int = 9
        self._CODE_LENGTH: int = 6

        self._aborted: bool = False


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
        print(Strings.OP_STARTING.format(self._name))

        self._parse_args(args)

        thread: Thread = Thread(target=self._task_manage_slots)

        print("type \"q\" to stop:")
        thread.start()

        if input() in ["q", "Q"]:
            self._aborted = True

        thread.join()

        print(Strings.OP_FINISHED.format(self._name))


    def _task_manage_slots(self):
        result_log = None

        params: _Slot = _Slot(
            "0" * 6,
            "0" * self._CODE_LENGTH
        )

        # ---- resume previous operation. ---- #

        self._resume_filepath: str = f"{self._args.output}/{self._name}_resume.txt"

        # need to resume previous operation.
        if self._args.need_state_resume and path.isfile(self._resume_filepath):
            with open(self._resume_filepath, "r") as resume_file:
                line: str = resume_file.readline()
                parts: list = line.split("::")

                params.group = parts[0]
                params.code = parts[1]

        # ---- start mining. ---- #

        try:
            while not self._aborted and params.group != "z" * self._MAX_GROUP_LENGTH:
                while not self._aborted and params.code != "z" * self._CODE_LENGTH:
                    params.result = 0

                    test: Thread = Thread(target=self._task_test_combo, args=[params])
                    test.start()
                    test.join(4.0)

                    # thread died.
                    if test.is_alive():
                        print("timed out.")
                        continue

                    # found something.
                    if params.result == 1:
                        # log not open yet.
                        if not result_log:
                            makedirs(self._args.output, exist_ok=True)
                            result_log = open(f"{self._args.output}/{self._name}_results.txt", "w+")

                        result_log.write(f"{params.group}::{hash}\n")

                    params.code = self._increment_ordinator_string(params.code)

                # not aborted.
                if not self._aborted:
                    params.group = self._increment_ordinator_string(params.group)

        except:
            pass

        # ---- store current operation. ---- #

        # need to store current operation.
        if self._args.need_state_resume :
            with open(self._resume_filepath, "w") as resume_file:
                resume_file.write(f"{params.group}::{params.code}")


    def _task_test_combo(self, params: _Slot):
        group_hash: str = f"{params.group}::{params.code}"
        print(f"testing: {group_hash} ... ", end="")

        probe_url: str = f"{self._domain}/book/{group_hash}"
        probe_response: Response = self._sess.get(probe_url)

        # book.
        if "class=\"books/details\"" in probe_response.text:
            print("book page.")
            params.result = 1

        # page not found.
        elif "<title>Page not found</title>" in probe_response.text:
            print("nothing.")

        # server overburdened.
        elif "Too many requests from your IP." in probe_response.text:
            print("server overburdened.")
            sleep(20)

        # something unexpected.
        else:
            print("something else.")
            print(probe_response.text)


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
