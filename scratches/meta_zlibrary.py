# scabies.
from scabies import Strings, args_output, args_time
from scabies.scraper import Scraper

# stdlib.
import itertools, string
from argparse import ArgumentParser
from os import makedirs, path

# scraping.
from bs4 import BeautifulSoup
from requests import Response


NAME: str = "zlibrary"
DOMAIN: str = "https://singlelogin.re"


class ZLibrary(Scraper):
    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        pass


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


        # ---- get mode. ---- #


        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.output_unstructured:
            self._destination_dir = self._args.output_unstructured

        args_output.validate_metadata_args(self._args)

        args_time.validate_time_selection_args(self._args)






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

        self._ensure_out_dir(self._args.output)



class MetaZLibary(Scraper):
    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

        self._parse_args(args)

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

        self._ensure_out_dir(self._args.output)


    def _parse_ls_size(self, arg: str):
        pass


    def _ensure_out_dir(self, out_dir: str):
        # dir doesn't exist.
        if not path.exists(out_dir):
            makedirs(out_dir)


def run(args: list):
    scraper: MetaZLibary = MetaZLibary()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
