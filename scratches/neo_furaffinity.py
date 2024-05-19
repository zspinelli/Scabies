# scabies.
from scabies import args_cookies, args_output, Strings, args_time
from scabies.scraper import Scraper
from scabies.switchplate import SwitchPlate

# stdlib.
from argparse import ArgumentParser
from os import path

# scraping.
from bs4 import BeautifulSoup
from requests import Response


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
        print(Strings.OP_STARTING.format(NAME))

        self._parse_args(args)

        # delegate to required mode.
        if self._args.mode == self.MODES.SEARCH: self._process_search_mode()
        elif self._args.mode == self.MODES.USER: self._process_user_mode()
        elif self._args.mode == self.MODES.POST: self._process_post_mode()

        print(Strings.OP_FINISHED.format(NAME))


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description=f"scabies for {NAME}")
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

        # ---- search mode. ---- #

        search_mode: ArgumentParser = modes.add_parser(self.MODES.SEARCH)

        args_time.add_time_selection_args(search_mode)

        self._add_post_types(search_mode)
        self._add_post_parts(search_mode)

        search_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("search urls")
        )

        # ---- user mode. ---- #

        user_mode: ArgumentParser = modes.add_parser(self.MODES.USER)

        args_time.add_time_selection_args(user_mode)

        self._add_user_parts(user_mode)
        self._add_post_types(user_mode)
        self._add_post_parts(user_mode)

        user_mode.add_argument(
            "names",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("user names")
        )

        # ---- post mode. ---- #

        post_mode: ArgumentParser = modes.add_parser(self.MODES.POST)

        self._add_post_parts(post_mode)

        post_mode.add_argument(
            "post",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("post ids")
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.output_unstructured:
            self._destination_dir = self._args.output_unstructured

        args_output.validate_metadata_args(self._args)

        args_cookies.validate_cookie_args(self._args, self._sess)

        args_time.validate_time_selection_args(self._args)


    def _add_user_parts(self, parser: ArgumentParser):
        parser.add_argument(
            "-up",
            default=self.USER_PARTS.default(),
            type=str,
            help=Strings.SEQ_STR_COMBO.format(self.USER_PARTS.legend()),
            dest="user_parts"
        )


    def _add_post_types(self, parser: ArgumentParser):
        parser.add_argument(
            "-pt",
            default=self.POST_TYPES.default(),
            type=str,
            help=Strings.SEQ_STR_COMBO.format(self.POST_TYPES.legend()),
            dest="post_types"
        )


    def _add_post_parts(self, parser: ArgumentParser):
        parser.add_argument(
            "-pp",
            default=self.POST_PARTS.default(),
            type=str,
            help=Strings.SEQ_STR_COMBO.format(self.POST_PARTS.legend()),
            dest="post_parts"
        )


    def _process_search_mode(self):

        search_url: str = path.join("search", )

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
            "mode": "extended"
        }

        while True:
            for post_id in self._retrieve_paginated_gallery():
                pass

            post_ids: list = self._retrieve_paginated_gallery(search_url, data)

            for result in results:
                self._scrape_post()

            # todo: break

            data["page"] += 1


    def _process_user_mode(self):
        for name in self._args.names:
            print(Strings.USER_STARTED.format(name))

            # structured output wanted.
            if self._args.output_structured:
                self._destination_dir = path.join(self._args.output_structured, NAME, name)

            # need to read time resume file.
            if self._args.need_time_resume:
                self._resume_filepath = path.join(self._destination_dir, args_time.resume_filename(name))
                self._resume = args_time.read_time_resume(self._resume_filepath)

            # gallery.
            if self.USER_PARTS.CODES.GALLERY in self._args.user_parts:
                #for post in self._retrieve_paginated_gallery(f"user/{name}/gallery"):
                    #print(post)

                page_num: int = 1

                while True:
                    page_num += 1

            # scraps.
            if self.USER_PARTS.CODES.SCRAPS in self._args.user_parts:
                #for thing in self._retrieve_paginated_gallery(f"user/{name}/scraps"):
                    #print(thing)

                page_num: int = 1

                while True:
                    page_num += 1

            # following.
            if self.USER_PARTS.CODES.FOLLOWING in self._args.user_parts:
                print(f"trying to get following from {name}")

                following_list_filepath: str = path.join(self._destination_dir, "following.txt")
                following_list = open(following_list_filepath, "w")

                for name in self._retrieve_paginated_namebox(DOMAIN + f"/watchlist/by/{name}"):
                    #for following in data:
                        #print("found following: {}".format(following["username"]))
                        #following_list.write(following["username"])
                    pass

                following_list.close()

            # followers.
            if self.USER_PARTS.CODES.FOLLOWERS in self._args.user_parts:
                print(f"trying to get followers from {name}")

                following_list_filepath: str = path.join(self._destination_dir, "followers.txt")
                following_list = open(following_list_filepath, "w")

                for name in self._retrieve_paginated_namebox(DOMAIN + f"/watchlist/to/{name}"):
                    #for following in data:
                        ##print("found follower: {}".format(following["username"]))
                        #following_list.write(following["username"])
                    pass

                following_list.close()

            # favorites.
            if self.USER_PARTS.CODES.FAVORITES in self._args.user_parts:
                pass

            # journals.
            if self.USER_PARTS.CODES.JOURNALS in self._args.user_parts:
                pass

            # need to write time resume file.
            if self._args.need_time_resume:
                args_time.write_time_resume(self._resume_filepath)

            print(Strings.USER_FINISHED.format(name))


    def _process_post_mode(self):
        pass


    def _process_journal_mode(self):
        pass


    def _retrieve_paginated_gallery(self, namebox_url: str):
        pass


    def _retrieve_paginated_namebox(self, namebox_url: str):
        while True:
            namebox_response: Response = self._sess.get(namebox_url)
            namebox_soup: BeautifulSoup = BeautifulSoup(namebox_response.content, "html.parser")

            names = namebox_soup.find()


    def _scrape_post(self):
        pass


    def _scrape_journal(self):
        pass


def run(args: list):
    scraper: Furaffinity = Furaffinity()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
