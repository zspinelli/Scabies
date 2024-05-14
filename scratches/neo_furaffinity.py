# scabies.
from scabies import args_cookies, args_login, args_output, session, Strings, args_time
from scabies.scraper import Scraper
from scabies.switchplate import SwitchPlate

# stdlib.
from argparse import ArgumentParser
from os import path


NAME: str = "furaffinity"
DOMAIN: str = "https://www.furaffinity.net"


class Furaffinity(Scraper):
    class MODES:
        SEARCH: str = "search"
        USER: str = "user"
        POST: str = "post"

    USER_PARTS: SwitchPlate = SwitchPlate({
        "GALLERY": "G",
        "FOLLOWING": "Fw",
        "FOLLOWERS": "Fr",
        "SCRAPS": "S",
        "FAVORITES": "Fa",
        "JOURNALS": "J"
    }, default="GS")

    POST_TYPES: SwitchPlate = SwitchPlate({
        "ART": "A",
        "MUSIC": "M",
        "FLASH": "F",
        "STORY": "S",
        "PHOTO": "Ph",
        "POETRY": "Po"
    }, default="AMFSPhPo")

    POST_PARTS: SwitchPlate = SwitchPlate({
        "MAIN": "M",
        "TAGS": "T",
        "DESC": "De",  # description.
        "DATE": "Da",
        "COMMENTS": "C",
        "STATISTICS": "S"
    }, default="MTDeDaCS")


    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        print(strings.OP_STARTING.format(NAME))

        self._sess = session.new()
        self._parse_args(args)

        # login if needed.
        if self._args.need_login:
            pass

        # delegate to required mode.
        if self._args.mode == self.MODES.SEARCH: self._process_search_mode()
        elif self._args.mode == self.MODES.USER: self._process_user_mode()
        elif self._args.mode == self.MODES.POST: self._process_post_mode()

        print(strings.OP_FINISHED.format(NAME))


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for furaffinity")
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
        args_login.add_login_args(parser, "email")

        # ---- search mode. ---- #

        search_mode: ArgumentParser = modes.add_parser(self.MODES.SEARCH)

        args_time.add_time_selection_args(search_mode)

        self._add_post_types(search_mode)
        self._add_post_parts(search_mode)

        search_mode.add_argument(
            "urls",
            nargs="+",
            help=strings.SEQ_SEP_SPACE.format("search urls")
        )

        # ---- user mode. ---- #

        user_mode: ArgumentParser = modes.add_parser(self.MODES.USER)

        time.add_time_selection_args(user_mode)

        self._add_user_parts(user_mode)
        self._add_post_types(user_mode)
        self._add_post_parts(user_mode)

        user_mode.add_argument(
            "names",
            nargs="+",
            help=strings.SEQ_SEP_SPACE.format("user names")
        )

        # ---- post mode. ---- #

        post_mode: ArgumentParser = modes.add_parser(self.MODES.POST)

        self._add_post_parts(post_mode)

        post_mode.add_argument(
            "post",
            nargs="+",
            help=strings.SEQ_SEP_SPACE.format("post ids")
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.ou:
            self._destination_dir = self._args.ou

        output.validate_metadata_args(self._args)

        cookies.validate_cookie_args(self._args, self._sess)
        #login.validate_login_args(self._args, _login)

        time.validate_time_selection_args(self._args)


    def _add_user_parts(self, parser: ArgumentParser):
        parser.add_argument(
            "-up",
            default=self.USER_PARTS.default(),
            type=str,
            help=strings.SEQ_STR_COMBO.format(self.USER_PARTS.legend()),
            dest="user_parts"
        )


    def _add_post_types(self, parser: ArgumentParser):
        parser.add_argument(
            "-pt",
            default=self.POST_TYPES.default(),
            type=str,
            help=strings.SEQ_STR_COMBO.format(self.POST_TYPES.legend()),
            dest="post_types"
        )


    def _add_post_parts(self, parser: ArgumentParser):
        parser.add_argument(
            "-pp",
            default=self.POST_PARTS.default(),
            type=str,
            help=strings.SEQ_STR_COMBO.format(self.POST_PARTS.legend()),
            dest="post_parts"
        )


    def _process_search_mode(self):
        data: dict = {
            "page": 1,
            "order-by": "relevancy",
            "order-direction": "desc",
            "range": "all",
            "range_from": "",
            "range_to": "",
            "rating-general": "1",
            "rating-mature": "1",
            "rating-adult": "1",
            "type-art": "1" if self.POST_TYPES.CODES.ART in self._args.post_types else "0",
            "type-music": "1" if self.POST_TYPES.CODES.MUSIC in self._args.post_types else "0",
            "type-flash": "1" if self.POST_TYPES.CODES.FLASH in self._args.post_types else "0",
            "type-story": "1" if self.POST_TYPES.CODES.STORY in self._args.post_types else "0",
            "type-photo": "1" if self.POST_TYPES.CODES.PHOTO in self._args.post_types else "0",
            "type-poetry": "1" if self.POST_TYPES.CODES.POETRY in self._args.post_types else "0",
            "mode": "extended",
        }


    def _process_user_mode(self):
        for name in self._args.names:
            print(strings.USER_STARTED.format(name))

            # structured output wanted.
            if self._args.output_structured:
                self._destination_dir = path.join(self._args.output_structured, NAME, name)

            # need to read time resume file.
            if self._args.need_time_resume:
                self._resume_file = path.join(self._destination_dir, args_time.resume_filename(name))
                self._resume = args_time.read_time_resume(self._resume_file)

            # gallery.
            if self.USER_PARTS.CODES.GALLERY in self._args.user_parts:
                for thing in self._retrieve_paginated_gallery("gallery", name):
                    print(thing)

            # scraps.
            if self.USER_PARTS.CODES.SCRAPS in self._args.user_parts:
                for thing in self._retrieve_paginated_gallery("scraps", name):
                    print(thing)

            # following.
            if self.USER_PARTS.CODES.FOLLOWING in self._args.user_parts:
                pass

            # followers.
            if self.USER_PARTS.CODES.FOLLOWERS in self._args.user_parts:
                pass

            # favorites.
            if self.USER_PARTS.CODES.FAVS in self._args.user_parts:
                pass

            # journals.
            if self.USER_PARTS.CODES.JOURNALS in self._args.user_parts:
                pass

            # need to write time resume file.
            if self._args.need_time_resume:
                args_time.write_time_resume(self._resume_filepath)

            print(strings.USER_FINISHED.format(name))


    def _process_post_mode(self):
        pass


    def _process_journal_mode(self):
        pass


    def _retrieve_paginated_namebox(self):
        pass


    def _retrieve_paginated_gallery(self, part, name: str):
        num: int = 1

        while True:
            page_url: str = DOMAIN + f"/{part}/{name}/{num}"
            page: str = self._sess.get(page_url).text

            pos: int = 0
            begin: str = "id=\"sid-"
            end: str = "\""

            while True:
                first = page.find(begin, pos)

                # nothing to do.
                if first == -1: break

                first += len(begin)
                last = page.find(end, first)
                post_id = page[first:last]
                pos = last + len(end)

                yield post_id

            num += 1


def run(args: list):
    scraper: Furaffinity = Furaffinity()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
