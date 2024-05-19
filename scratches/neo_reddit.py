# stdlib.
from argparse import ArgumentParser

# scabies.
from scabies import Strings
from scabies.scraper import Scraper


NAME: str = "reddit"
DOMAIN: str = "https://www.reddit.com"


class Reddit(Scraper):
    class MODES:
        SUB: str = "sub"
        THREAD: str = "thread"
        USER: str = "user"
        POST: str = "post"


    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(NAME))

        self._parse_args(args)

        # delegate to required mode.
        if self._args.mode == self.MODES.SUB:       self._process_sub_mode()
        elif self._args.mode == self.MODES.THREAD:  self._process_thread_mode()
        elif self._args.mode == self.MODES.USER:    self._process_user_mode()
        elif self._args.mode == self.MODES.POST:    self._process_post_mode()

        print(Strings.OP_FINISHED.format(NAME))


    def _parse_args(self, args: list):
        parser: ArgumentParser


    def _process_sub_mode(self):
        pass


    def _process_thread_mode(self):
        pass


    def _process_user_mode(self):
        pass


    def _process_post_mode(self):
        pass
