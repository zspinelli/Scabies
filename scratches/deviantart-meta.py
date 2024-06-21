# scabies.
from concurrent.futures import ThreadPoolExecutor

from scabies import Strings
from scabies.scraper import Scraper

# stdlib.
import atexit
from argparse import ArgumentParser
from os import makedirs, path
from time import sleep

# scraping.
from blessed import Terminal
from requests import Response


class _Slot:
    def __init__(self, name: str):
        self.name = name


class DeviantartMeta(Scraper):
    def __init__(self):
        super().__init__("deviantart-meta", "https://www.deviantart.com", 2)

        self._MAX_UNAME_LEN: int = 20

        self._aborted: bool = False
        self._slots: list = [_Slot("0-0")]


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser()

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

        self._resume_filepath: str = f"{self._args.output}/{self._name.strip("_meta")}/{self._name}_resume.txt"

        # need to resume previous operation.
        if self._args.need_state_resume and path.isfile(self._resume_filepath):
            with open(self._resume_filepath, "r") as resume_file:
                line: str = resume_file.readline()

                self._slots[0].name = line

        # ---- start mining. ---- #

        pool.submit(self._task, self._slots[0])

        while True:
            # user requested abort.
            if input() in ["q", "Q"]:
                break

        print(Strings.OP_FINISHED.format(self._name))


    def _task(self, slot):
        result_log = None

        while name != "z" * self._MAX_UNAME_LEN:
            print(f"testing: {name} ... ", end="")

            probe_url: str = f"{self._domain}/{name}"
            probe_response: Response = self._sess.get(probe_url)

            # throttle or server busy.
            if probe_response.status_code == 403:
                print(probe_response.status_code, "waiting and retrying...")
                sleep(20)
                continue

            # found a user page.
            elif probe_response.status_code == 200:
                print("found a user.")

                # log not open yet.
                if not result_log:
                    makedirs(self._args.output, exist_ok=True)
                    result_log = open(path.join(self._args.output, "results.txt"), "a")

                result_log.write(f"{name}\n")
                result_log.flush()

            # found nothing.
            else:
                print(probe_response.status_code)

            name = self._increment_ordinator_string(name)










    def run(self, args: list):
        def write_resume():
            # need to save this operation.
            if self._args.need_state_resume:
                resume_file = open(self._resume_filepath, "w")
                resume_file.write(name + "\n")
                resume_file.close()

        atexit.register(write_resume)



        """# need to save this operation.
        if self._args.need_state_resume:
            resume_file = open(self._resume_filepath, "w")
            resume_file.write(name + "\n")
            resume_file.close()"""

        atexit.unregister(write_resume)





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

            # rollover from '-' to '0'.
            if ord_val == 45:
                ord_string = front + "0" + back
                break

            # rollover from '9' to 'a'.
            elif ord_val == 57:
                ord_string = front + "a" + back
                break

            # rollover from 'z' to '-' or '0'.
            elif ord_val == 122:
                # rollover to '-' or '0'.
                if len(ord_string) > i > 0: ord_string = front + "-" + back
                else:                       ord_string = front + "0" + back

                i -= 1

            # increment 0-9, or a-z.
            elif ord_val < 57 or ord_val < 122:
                ord_string = front + chr(ord_val + 1) + back
                break

        return ord_string


def run(args: list):
    scraper: DeviantartMeta = DeviantartMeta()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
