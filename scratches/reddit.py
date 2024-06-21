# stdlib.
from argparse import ArgumentParser

# scabies.
from scabies import Strings
from scabies.scraper import Scraper


class Reddit(Scraper):
    class MODES:
        SUB: str = "sub"
        THREAD: str = "thread"
        USER: str = "user"
        POST: str = "post"


    def __init__(self):
        super().__init__("reddit", "https://www.reddit.com")


    def _parse_args(self, args: list):
        parser: ArgumentParser


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self._name))

        self._parse_args(args)

        # delegate to required mode.
        if self._args.mode == self.MODES.SUB:       self._process_sub_mode()
        elif self._args.mode == self.MODES.THREAD:  self._process_thread_mode()
        elif self._args.mode == self.MODES.USER:    self._process_user_mode()
        elif self._args.mode == self.MODES.POST:    self._process_post_mode()

        print(Strings.OP_FINISHED.format(self._name))


    def _process_sub_mode(self):
        for sub in self._args.subs:
            endpoint: str = f"{sub}.json"


    def _process_thread_mode(self):
        pass


    def _process_user_mode(self):
        for user in self._args.users:
            endpoint: str = f"/user/{user}/.json"


    def _process_post_mode(self):
        pass


    def _paginate(self, endpoint: str):
        while True:
            pass


    def _call(self):
        pass


def run(args: list):
    scraper: Reddit = Reddit()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
