# scabies.
from scabies import Strings, args_output, args_time
from scabies.scraper import Scraper

# stdlib.
import itertools, string
from argparse import ArgumentParser
from os import path

# scraping.
from bs4 import BeautifulSoup
from requests import Response


NAME: str = "zlibrary"
DOMAIN: str = "https://singlelogin.re"


class ZLibrary(Scraper):
    class MODES:
        SCRAPE: str = "scrape"
        GET: str = "get"


    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

        self._parse_args(args)

        # delegate to required mode.
        if self._args.mode == self.MODES.SCRAPE:    self._process_scrape_mode()
        elif self._args.mode == self.MODES.GET:     self._process_get_mode()

        print(Strings.OP_FINISHED.format(NAME))


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for zlibrary")
        modes = parser.add_subparsers(
            title="modes",
            dest="mode",
            required=True,
            help="see individual mode helps for additional options"
        )

        # ---- external features. ---- #

        args_output.add_output_args(parser)
        args_output.add_metadata_args(parser)

        # ---- scrape mode. ---- #

        scrape_mode: ArgumentParser = modes.add_parser(self.MODES.SCRAPE)

        scrape_mode.add_argument(
            '-ls',
            default="1024mb",
            type=self._parse_log_size,
            help="log size. restrict the result logs filesize. units: (b, kb, mb, gb)",
            dest="log_size"
        )

        # ---- get mode. ---- #

        get_mode: ArgumentParser = modes.add_parser(self.MODES.GET)

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.output_unstructured:
            self._destination_dir = self._args.output_unstructured

        args_output.validate_metadata_args(self._args)

        args_time.validate_time_selection_args(self._args)


    def _process_scrape_mode(self):
        group: str = "0" * 7

        while group != "z" * 7:
            hash: str = "0" * 6

            while hash != "z" * 6:
                hash = self._increment_ordinator_string(hash)

            group = self._increment_ordinator_string(group)


    def _process_get_mode(self):
        pass


    def _parse_log_size(self, arg: str):
        pass


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




class MetaZLibary(Scraper):
    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):




        print("started zlibrary probe")

        result_log = open(path.join(self._args.output, "results.txt"), "w+")

        for seq_7 in itertools.combinations(string.digits, 7):
            seq_7: str = "".join(seq_7)

            for seq_6 in itertools.combinations(string.ascii_lowercase + string.digits, 6):
                seq_6: str = "".join(seq_6)
                print(f"testing: {seq_7}/{seq_6} ... ", end="")

                probe_url: str = f"{DOMAIN}/book/{seq_7}/{seq_6}"
                probe_response: Response = self._sess.get(probe_url)

                page_soup: BeautifulSoup = BeautifulSoup(probe_response.text, "html.parser")
                book_page = page_soup.find("body", {"class": "books/details"})

                # found a book page.
                if book_page:
                    print("found book page.")
                    result_log.write(f"{seq_7}/{seq_6}\n")

                # got redirected to home.
                else:
                    print("nothing here.")


        print("finished zlibrary probe")




    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for azlyrics")

        # ---- output. ---- #

        parser.add_argument(
            "-o",
            help="output path. writes scrape result log in the given directory.",
            dest="output"
        )


def run(args: list):
    scraper: MetaZLibary = MetaZLibary()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
