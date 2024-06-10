# scabies.
from scabies import Strings
from scabies.scraper import Scraper, MetaScraper

# stdlib.
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from os import path

# scraping.
import stem
from requests import Session, Response


class _Slot:
    def __init__(self, start_name: str):
        self.name: str = start_name


class DeviantartMeta(MetaScraper):
    def __init__(self):
        super().__init__(
            "deviantart-meta-all-usernames",
            "https://www.deviantart.com",
            self._thread_task,
            self._print_stats
        )


    def _parse_args(self, args: list):
        pass


    def _thread_task(self):
        pass


    def _print_stats(self):
        pass


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








class DeviantartMeta(Scraper):
    def __init__(self):
        super().__init__()

        self._sess = None

        self._MAX_UNAME_LEN: int = 20
        self._next_uname: str = "0-0"




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



    def _name_task(self, slot: _Slot):
        print(f"testing: {slot.name} ... ", end="")

        result_log = None

        while slot.name != "z" * self._MAX_UNAME_LEN:
            probe_url: str = f"{self._domain}/{slot.name}"
            probe_response: Response = self._sess.get(probe_url)

            # found a user page.
            if probe_response.status_code == 200:
                print("found book page.")

                # log not open yet.
                if not result_log:
                    result_log = open(path.join(self._args.output, "results.txt"), "a")

                result_log.write(f"{slot.name}\n")

            slot.name = self._increment_ordinator_string(slot.name)

        del slot


def run(args: list):
    scraper: DeviantartMeta = DeviantartMeta()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
