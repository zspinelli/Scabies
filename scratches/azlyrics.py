# stdlib.
from argparse import ArgumentParser

# scabies.
from scabies import Strings, args_output
from scabies.scraper import Scraper


class AZLyrics(Scraper):
    class MODES:
        ARTISTS: str = "artists"
        ALBUMS: str = "albums"
        SONGS: str = "songs"


    def __init__(self):
        super().__init__("azlyrics", "https://www.azlyrics.com")


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for azlyrics")
        modes = parser.add_subparsers(
            title="modes",
            dest="mode",
            required=True,
            help="see individual mode helps for additional options"
        )

        # ---- external features. ---- #

        args_output.add_output_args(parser)

        # ---- artists mode. ---- #

        artists_mode: ArgumentParser = modes.add_parser(self.MODES.ARTISTS)

        artists_mode.add_argument(
            "names",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("search urls")
        )

        # ---- albums mode. ---- #

        albums_mode: ArgumentParser = modes.add_parser(self.MODES.ALBUMS)

        albums_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("search urls")
        )

        # ---- songs mode. ---- #

        songs_mode: ArgumentParser = modes.add_parser(self.MODES.SONGS)

        songs_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("search urls")
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.output_unstructured:
            self._destination_dir = self._args.output_unstructured

        args_output.validate_metadata_args(self._args)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self._name))

        self._parse_args(args)

        # delegate to required mode.
        if self._args.mode == self.MODES.ARTISTS:   self._process_artists_mode()
        elif self._args.mode == self.MODES.ALBUMS:  self._process_albums_mode()
        elif self._args.mode == self.MODES.SONGS:   self._process_songs_mode()

        print(Strings.OP_FINISHED.format(self._name))


    def _process_artists_mode(self):
        for hash_id in self._args.projects:
            print("started project: " + hash_id)

            print("finished project: " + hash_id)


    def _process_albums_mode(self):
        for hash_id in self._args.projects:
            print("started project: " + hash_id)

            print("finished project: " + hash_id)


    def _process_songs_mode(self):
        for hash_id in self._args.projects:
            print("started project: " + hash_id)

            print("finished project: " + hash_id)


def run(args: list):
    scraper: AZLyrics = AZLyrics()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
