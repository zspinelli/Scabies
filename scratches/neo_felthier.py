"""
zspinelli:
Eventually I want to add a post mode to this that will receive either an art url or html url
and then scrape that and search for a matching opposite to scrape, meaning it would get both regardless
of which it is given so that users don't need to be discriminant to get desired behavior.

There is a problem either with the tor connection that needs resolved. After a while
the connection seems to drop. I don't know if it's the result of the server failing to respond or tor
hanging up. This problem becomes more apparent when scraping larger galleries.
"""

# scabies.
from scabies import args_output, Strings, args_time, tor
from scabies.scraper import Scraper
from scabies.switchplate import SwitchPlate

# scraping.
from bs4 import BeautifulSoup, ResultSet
from requests import Response
from urllib.parse import ParseResult, urlparse

# stdlib.
from argparse import ArgumentParser
from datetime import datetime
from os import path


NAME: str = "felthier"
DOMAIN: str = "g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa"


class Felthier(Scraper):
    class MODES:
        USER: str = "user"
        POST: str = "post"

    POST_TYPES: SwitchPlate = SwitchPlate({
        "UNKOWN": "U",
        "IMAGE": "I",
        "MUSIC": "M",
        "FLASH": "F",
        "WRITING": "W",
    }, default="UIMFW")

    POST_PARTS: SwitchPlate = SwitchPlate({
        "MAIN": "M",
        "DESCRIPTION": "Ds",
        "DATE": "Dt"
    }, default="MDsDt")


    class PostInfo:
        def __init__(self, author: str, anchor, dest_dir: str):
            self.author: str = author
            self.link: str = anchor["href"]
            self.title: str = self._sanitize_name(anchor.text).rstrip(".")
            self.filepath_out: str = path.join(dest_dir, self.title)
            self.ext: str = path.splitext(anchor["href"])[1]
            self.date: datetime = datetime.strptime(anchor[2].text[:16], args_time.TIME_FORMAT)


        def _sanitize_name(self, name: str) -> str:
            new_name = name
            bad_chars = {'\x03': "%03"}

            for c in name:
                if c in bad_chars:
                    new_name = new_name.replace(c, bad_chars[c])

            return new_name


    def __init__(self):
        super().__init__("felthier")


    def run(self, args: list):
        print(Strings.OP_STARTING.format(NAME))

        self._sess.proxies = {
            "http": "socks5h://localhost:9150",
            "https": "socks5h://localhost:9150"
        }

        self._parse_args(args)

        tor.start()

        # delegate to required mode.
        if self._args.mode == self.MODES.USER:    self._process_user_mode()
        elif self._args.mode == self.MODES.POST:  self._process_post_mode()

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

        tor.add_tor_args(parser)

        # ---- user mode. ---- #

        user_mode: ArgumentParser = modes.add_parser(self.MODES.USER)

        args_time.add_time_selection_args(user_mode)

        user_mode.add_argument(
            "-pt",
            default=self.POST_TYPES.default(),
            help=Strings.SEQ_STR_COMBO.format(self.POST_TYPES.legend()),
            dest="post_types"
        )

        self._add_post_parts(user_mode)

        user_mode.add_argument(
            "names",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("user names")
        )

        # ---- post mode. ---- #

        """
        post_mode = modes.add_parser(self.MODES.POST)
        
        self._add_post_parts(user_mode)

        post_mode.add_argument(
            "posts",
            nargs="+",
            help=strings.SEQ_SEP_SPACE.format("post slugs")
        )
        """

        # ---- parse ---- #

        self._args = parser.parse_args()
        # print(f"input: {_argv}")

        # ---- validate. ----  #

        # unstructured output wanted.
        if self._args.output_unstructured:
            _dest_dir = self._args.output_unstructured

        args_output.validate_metadata_args(self._args)
        tor.validate_tor_args(self._args)

        args_time.validate_time_selection_args(self._args)


    def _add_post_parts(self, parser: ArgumentParser):
        parser.add_argument(
            "-pp",
            default=self.POST_PARTS.default(),
            help=Strings.SEQ_STR_COMBO.format(self.POST_PARTS.legend()),
            dest="post_parts"
        )


    def _process_user_mode(self):
        for name in self._args.names:
            print(Strings.USER_STARTED.format(name))

            # structured output wanted.
            if self._args.output_structured:
                self._destination_dir = path.join(self._args.output_structured, NAME, name)

            # need to read time resume file.
            if self._args.need_time_resume:
                self._resume_filepath = path.join(self._destination_dir, args_time.resume_filename(name))
                self._resume_time = args_time.read_time_resume(self._resume_filepath)

            subdirs: list = [name + "/"]

            while subdirs:
                # ---- get subdir page items. ---- #

                curr_subdir: str = subdirs.pop(0)
                subdir_url: str = DOMAIN + f"/{curr_subdir}"

                print("scraping subdir: " + curr_subdir)

                subdir_response: Response = self._sess.get(subdir_url)
                subdir_soup: BeautifulSoup = BeautifulSoup(subdir_response.text, "html.parser")

                # ---- process page items. ---- #

                posts: ResultSet = subdir_soup.find_all("tr")[3:-1]

                for post in posts:
                    post_tds: ResultSet = post.find_all("td")
                    anchor = post_tds[1].find("a")

                    # ---- create info package. ---- #

                    info: Felthier.PostInfo = Felthier.PostInfo(name, anchor, self._destination_dir)

                    # ---- determine continuity. ---- #

                    # skip for last run resume.
                    if self._args.need_time_resume and info.date <= self._resume_time:
                        print(Strings.SKIP.format(Strings.SKIP_TIME_RESUME))
                        continue

                    # skip for time cutoff.
                    if self._args.need_time_cutoff and args_time.exceeds_time_cutoff_limits(self._args, info.date):
                        print(Strings.SKIP.format("date cutoff"))
                        continue

                    # ---- detect content type. ---- #

                    # found file.
                    if info.ext:
                        print("found file: " + info.title)

                        # found "metadata" (html).
                        if self._args.need_metadata and info.ext == "html":
                            desc_response: Response = self._sess.get(info.link)
                            desc: str = BeautifulSoup(desc_response.text, "html.parser").find("pre").text.strip()

                            self._save_metadata(desc, info)

                        # found "main" (non-html).
                        elif self.POST_PARTS.CODES.MAIN in self._args.post_parts:
                            # found binary.
                            if(
                                self.POST_TYPES.CODES.UNKNOWN in self._args.post_types and info.ext == "." or
                                self.POST_TYPES.CODES.IMAGE in self._args.post_types and info.ext in [".png", ".jpg", ".jpeg", ".gif"] or
                                self.POST_TYPES.CODES.MUSIC in self._args.post_types and info.ext in [".mp3", ".ogg", ".flac"] or
                                self.POST_TYPES.CODES.FLASH in self._args.post_types and info.ext == ".sfw" or
                                self.POST_TYPES.CODES.WRITING in self._args.post_types and info.ext in [".txt", ".docx", ".odt", ".pdf"]
                            ):
                                self._scrape_data(info)

                    # found subdir.
                    else:
                        print("found subdir: " + info.title)
                        new_subdir: str = f"{subdir_url}{info.link}"
                        subdirs.append(new_subdir)

            # need to write time resume file.
            if self._args.need_time_resume:
                args_time.write_time_resume(self._resume_filepath)

            print(Strings.USER_FINISHED.format(name))


    def _process_post_mode(self):
        for url in self._args.posts:
            # if url is not html, try html version for metadata.
            if not url.endswith(".html") and self._args.need_metadata:
                parsed_url: ParseResult = urlparse(url)
                url_parts: list = parsed_url.path.split("/")

                print(url_parts)


    def _scrape_data(self, info: PostInfo):
        # don't overwrite existing files.
        if not self._args.allow_overwrite and path.exists(info.filepath_out):
            print(Strings.SKIP.format(Strings.SKIP_NO_CLOBBER))
            return

        payload: Response = self._sess.get(info.link, stream=True)
        args_output.write_binary(info.filepath_out + info.ext, payload.content)


    def _save_metadata(self, desc: str, info: PostInfo):
        meta: dict = {
            "author": info.author,
            "description": desc
        }

        tags: list = []
        tags.append("author:" + info.author)
        tags.append("published:" + info.date[:4])

        extra: dict = {}
        extra.update({"full_published": info.date})

        # want json metadata.
        if self._args.json_meta:
            data: dict = {**meta, **extra}
            args_output.write_json(self._args.allow_overwrite_meta, info.filepath_out, data)

        # want toml metadata.
        if self._args.toml_meta:
            data: dict = {**meta, **extra}
            args_output.write_toml(self._args.allow_overwrite_meta, info.filepath_out, data)


if __name__ == "__main__":
    from sys import argv, exit

    scraper: Felthier = Felthier()
    scraper.run(argv)

    exit(0)
