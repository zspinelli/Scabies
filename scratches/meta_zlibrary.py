# scabies.
from scabies import Strings
from scabies.scraper import Scraper

# stdlib.
import itertools, string
from argparse import ArgumentParser
from os import path

# scraping.
from requests import Response


NAME: str = "zlibrary"
DOMAIN: str = "https://singlelogin.re"


class MetaZLibary(Scraper):
    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

        self._parse_args(args)

        print("started zlibrary probe")

        result_log = open(path.join(self._args.output, "results.txt"), "r+")

        for seq_7 in itertools.combinations(string.digits, 7):
            seq_7: str = "".join(seq_7)

            for seq_6 in itertools.combinations(string.ascii_lowercase + string.digits, 6):
                seq_6: str = "".join(seq_6)
                print(f"testing: {seq_7}/{seq_6} ... ", end="")

                probe_url: str = f"{DOMAIN}/book/{seq_7}/{seq_6}"
                probe_response: Response = self._sess.get(probe_url)

                print(f"status: {probe_response.status_code}")

                # ---- write result. ---- #

                result_log.write("{seq_7}/{seq_6}\n")

        print("finished zlibrary probe")

        print(Strings.OP_FINISHED.format(NAME))


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for azlyrics")

        # ---- output. ---- #

        parser.add_argument(
            "-o",
            help="output path. writes scrape result log in the given directory.",
            dest="output"
        )

        parser.add_argument(
            '-ls',
            default="1024mb",
            type=self._parse_ls_size,
            help="log size. restrict the result logs filesize. units: (b, kb, mb, gb)",
            dest="log_size"
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")


    def _parse_ls_size(self, arg: str):
        pass


def run(args: list):
    scraper: MetaZLibary = MetaZLibary()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
