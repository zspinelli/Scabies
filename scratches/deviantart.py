# scabies.
from scabies import Strings, session, args_output, args_cookies, args_oauth, args_time
from scabies.scraper import Scraper, ScraperInfo

# stdlib.
from argparse import ArgumentParser

# scraping.
from requests import Response


INFO = ScraperInfo(
    name="deviantart",
    domain="https://www.deviantart.com",
    modes=["search", "users", "folder", "art", "post"],
    particles={
        "user_part": {
            "set": ["gallery", "favorites", "posts", "watchers", "watching"],
            "default": [0]
        },
        "art_type": {
            "set": ["image","writing"],
            "default": [0, 1]
        },
        "art_part": {
            "set": ["main", "description", "tags", "date", "comments", "statistics", "download"],
            "default": [0, 1, 2, 3, 6]
        }
    }
)


class Deviantart(Scraper):
    OAUTH_CLIENT_ID: str = "5388"
    OAUTH_CLIENT_SECRET: str = "76b08c69cfb27f26d6161f9ab6d061a1"


    def __init__(self):
        super().__init__(INFO.NAME, INFO.DOMAIN)


    def _parse_args(self, args: list):
        parser: ArgumentParser = arg_parser()

        self._args = parser.parse_args()
        print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.ou:
            self._destination_dir = self._args.ou

        args_output.validate_metadata_args(self._args)

        args_cookies.validate_cookie_args(self._args, self._sess)
        args_oauth.validate_oauth_args(self._args, self._name)

        args_time.validate_time_selection_args(self._args)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self._name))

        self._sess = session.new(0)
        self._parse_args(argv)

        # delegate to required mode.
        if self._args.mode == INFO.MODE.SEARCH:     self._process_search_mode()
        elif self._args.mode == INFO.MODE.USER:     self._process_user_mode()
        elif self._args.mode == INFO.MODE.FOLDER:   self._process_folder_mode()
        elif self._args.mode == INFO.MODE.ART:      self._process_art_mode()
        elif self._args.mode == INFO.MODE.POST:     self._process_post_mode()

        print(Strings.OP_FINISHED.format(self._name))


    def _oauth_wizard(self):
        print(
            "1) login to deviantart in your browser.\n\n"

            "2) open the following url:\n"
            "https://www.deviantart.com/developers/apps\n\n"

            "3) click the \"Register Application\" button.\n\n"

            "4) fill out the form.\n\n"

            "5) paste the \"client_id\" and \"client_secret\" codes in the prompts below.\n\n"
        )

        oauth_client_id: str = input("enter client_id:")
        oauth_client_secret: str = input("enter client_secret:")


    def _process_search_mode(self):
        pass


    def _process_user_mode(self):
        pass


    def _process_folder_mode(self):
        pass


    def _process_art_mode(self):
        pass


    def _process_post_mode(self):
        pass


    def _search_eclipse(self):
        pass


    def _search_oauth(self):
        pass


    def _user_eclipse(self):
        pass


    def _user_oauth(self):
        pass


    def _folder_eclipse(self):
        pass


    def _folder_oauth(self):
        pass


    def _art_eclipse(self):
        pass


    def _art_oauth(self):
        pass


    def _post_eclipse(self):
        pass


    def _post_oauth(self):
        pass


def arg_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(description="scabies for deviantart")

    modes = parser.add_subparsers(
        title="modes",
        dest="mode",
        required=True,
        help="see individual mode helps for additional options"
    )

    # ---- external features. ---- #

    args_output.add_output_args(parser)
    args_output.add_metadata_args(parser)

    args_cookies.add_cookie_args(parser)
    args_oauth.add_oauth_args(parser)

    # ---- search mode. ---- #

    search_mode: ArgumentParser = modes.add_parser(INFO.MODE.SEARCH)

    args_time.add_time_selection_args(search_mode)

    _add_art_types(search_mode)
    _add_art_parts(search_mode)

    search_mode.add_argument(
        "urls",
        nargs="+",
        help=Strings.SEQ_SEP_SPACE.format("search urls")
    )

    # ---- user mode. ---- #

    user_mode: ArgumentParser = modes.add_parser(INFO.MODE.USER)

    args_time.add_time_selection_args(user_mode)

    _add_art_types(user_mode)
    _add_art_parts(user_mode)

    user_mode.add_argument(
        "names",
        nargs="+",
        help=Strings.SEQ_SEP_SPACE.format("user names")
    )

    # ---- folder mode. ---- #

    folder_mode: ArgumentParser = modes.add_parser(INFO.MODE.FOLDER)

    args_time.add_time_selection_args(folder_mode)

    _add_art_parts(folder_mode)
    _add_art_types(folder_mode)

    folder_mode.add_argument(
        "urls",
        nargs="+",
        help=Strings.SEQ_SEP_SPACE.format("folder urls")
    )

    # ---- art mode. ---- #

    art_mode: ArgumentParser = modes.add_parser(INFO.MODE.ART)

    _add_art_parts(art_mode)

    art_mode.add_argument(
        "urls",
        nargs="+",
        help=Strings.SEQ_SEP_SPACE.format("art urls")
    )

    # ---- post mode. ---- #

    post_mode: ArgumentParser = modes.add_parser(INFO.MODE.POST)

    post_mode.add_argument(
        "urls",
        nargs="+",
        help=Strings.SEQ_SEP_SPACE.format("post urls")
    )

    return parser


def _add_user_parts(parser: ArgumentParser):
    parser.add_argument(
        "-up",
        nargs="+",
        default=INFO.USER_PART.DEFAULT,
        choices=INFO.USER_PART.LEGEND,
        help=Strings.SEQ_SEP_SPACE.format(INFO.USER_PART.LEGEND),
        dest="user_parts"
    )


def _add_art_types(parser: ArgumentParser):
    parser.add_argument(
        "-at",
        nargs="+",
        default=INFO.ART_TYPE.DEFAULT,
        choices=INFO.ART_TYPE.LEGEND,
        help=Strings.SEQ_SEP_SPACE.format(INFO.ART_TYPE.LEGEND),
        dest="art_types"
    )


def _add_art_parts(parser: ArgumentParser):
    parser.add_argument(
        "-ap",
        nargs="+",
        default=INFO.ART_PART.DEFAULT,
        choices=INFO.ART_PART.LEGEND,
        help=Strings.SEQ_SEP_SPACE.format(INFO.ART_PART.LEGEND),
        dest="art_parts"
    )


def run(args: list):
    scraper: Deviantart = Deviantart()
    scraper.run(args)


# entry point.
if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
