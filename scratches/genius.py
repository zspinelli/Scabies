# scabies.
from scabies import args_output, Strings
from scabies.scraper import Scraper

# stdlib.
from argparse import ArgumentParser


class Genius(Scraper):
    class MODES:
        ARTISTS: str = "artists"
        ALBUMS: str = "albums"
        SONGS: str = "songs"


    def __init__(self):
        super().__init__("genius", "https://www.genius.com")


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for genius")
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
            help=Strings.SEQ_SEP_SPACE.format("artist names")
        )

        # ---- albums mode. ---- #

        albums_mode: ArgumentParser = modes.add_parser(self.MODES.ALBUMS)

        albums_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("album urls")
        )

        # ---- songs mode. ---- #

        songs_mode: ArgumentParser = modes.add_parser(self.MODES.SONGS)

        songs_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("song urls")
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        # print(f"input: {self._args}")

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
        for name in self._args.artists:
            print("started artist: " + name)

            print("finished artist: " + name)


    def _process_albums_mode(self):
        for album in self._args.albums:
            print("started album: " + album)

            print("finished album: " + album)


    def _process_songs_mode(self):
        for song in self._args.songs:
            print("started song: " + song)

            print("finished song: " + song)


def run(args: list):
    scraper: Genius = Genius()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
