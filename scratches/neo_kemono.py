# stdlib.
from argparse import ArgumentParser
from datetime import datetime
from os import path
from urllib.parse import urlparse, ParseResult

# scabies.
from scabies import args_cookies, args_output, args_time, Strings
from scabies.scraper import Scraper
from scabies.switchplate import SwitchPlate

# scraping.
from requests import Response


NAME: str = "kemono"
DOMAIN: str = "https://kemono.su"


class Kemono(Scraper):
    class MODES:
        FAVS: str = "favorites"
        CREATOR: str = "creator"
        POST: str = "post"

    CONTENT_TYPES: SwitchPlate({
        "IMAGE": "I",
        "VIDEO": "V"
    }, default="IV")


    def __init__(self):
        super().__init__(NAME, 0)

        self._sess.headers.update({"Accept-Encoding": "identity"})


    def run(self, args: list):
        print(Strings.OP_STARTING.format(NAME))

        self._parse_args(args)

        # delegate to required mode.
        if self._args.mode == self.MODES.FAVS:      self._process_favorites_mode()
        elif self._args.mode == self.MODES.CREATOR: self._process_creator_mode()
        elif self._args.mode == self.MODES.POST:    self._process_post_mode()

        print(Strings.OP_FINISHED.format(NAME))


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for kemono")
        modes = parser.add_subparsers(
            title="modes",
            dest="mode",
            required=True,
            help="see individual mode helps for additional options"
        )

        # ---- external features. ---- #

        args_output.add_output_args(parser)
        args_output.add_metadata_args(parser)

        # ---- favorites mode. ---- #

        favorites_mode: ArgumentParser = modes.add_parser(self.MODES.FAVS)

        args_cookies.add_cookie_args(favorites_mode, True)

        args_time.add_time_selection_args(favorites_mode)

        # ---- creator mode. ---- #

        creator_mode: ArgumentParser = modes.add_parser(self.MODES.CREATOR)

        args_time.add_time_selection_args(creator_mode)

        creator_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("user urls")
        )

        # ---- post mode. ---- #

        post_mode: ArgumentParser = modes.add_parser(self.MODES.POST)

        post_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("post urls")
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.output_unstructured:
            self._destination_dir = self._args.output_unstructured

        args_output.validate_metadata_args(self._args)

        args_cookies.validate_cookie_args(self._args, self._sess)

        args_time.validate_time_selection_args(self._args)


    def _process_favorites_mode(self):
        favorites_url: str = f"{DOMAIN}/api/v1/account/favorites"
        favorites_response: Response = self._sess.get(favorites_url)

        # not logged in.
        if favorites_response.status_code == 401:
            print(Strings.LOGIN_REQUIRED.format(NAME))

        # got favorites back.
        elif favorites_response.status_code == 400:
            print("favorites:", favorites_response.json())


    def _process_creator_mode(self):
        for user_url in self._args.urls:
            # ---- parse url. ---- #

            path_parts: list = self._parse_path_parts(user_url)

            service: str = path_parts[0]
            creator_id: str = path_parts[2]

            del path_parts

            # ---- get data. ---- #

            print(f"started creator: {creator_id}")

            params: dict = {"o": 0}

            while True:
                posts_url: str = f"{DOMAIN}/api/v1/{service}/user/{creator_id}"
                posts_response: Response = self._sess.get(posts_url, params=params)

                # request successful.
                if posts_response.status_code == 200:
                    print(posts_response.json())
                    posts: dict = posts_response.json()

                    for post in posts:
                        print("post:", post)
                        self._scrape_post(post)

                    # no more posts.
                    if len(posts) < 50:
                        break

                    params["o"] += 50

            print(f"finished creator: {creator_id}")


    def _process_post_mode(self):
        for post_url in self._args.urls:
            # ---- parse url. ---- #

            path_parts: list = self._parse_path_parts(post_url)

            service: str = path_parts[0]
            creator_id: str = path_parts[2]
            post_id: str = path_parts[4]

            del path_parts

            # ---- get data. ---- #

            print(f"started post: {post_id}")

            post: dict = self._retrieve_post(service, creator_id, post_id)
            self._scrape_post(post)

            print(f"finished post: {post_id}")


    def _scrape_post(self, post: dict):
        # ---- time cutoff. ---- #

        post_time: datetime = datetime.strptime(post["published"], "%Y-%m-%dT%H:%M:%S")

        # skip for time resume.
        if self._args.need_time_resume and post_time <= self._resume_time:
            print(Strings.SKIP_TIME_RESUME)
            return

        # skip for time cutoff.
        if self._args.need_time_cutoff and args_time.exceeds_time_cutoff_limits(self._args, post_time):
            print(Strings.SKIP_TIME_CUTOFF)
            return

        # ---- get data. ---- #

        creator: dict = self._retrieve_profile(post["service"], post["user"])

        project_dir_name: str = f"{post["id"]}_{post["title"]}"
        attachment_filenames: list = []

        # structured output wanted.
        if self._args.output_structured:
            self._destination_dir = path.join(self._args.output_structured, NAME, f"{post["user"]}_{creator["name"]}")

        for attachment in post["attachments"]:
            data_filename: str = attachment["name"]

            # metadata wanted.
            if self._args.need_metadata:
                attachment_filenames.append(data_filename)

            data_filepath: str = path.join(self._destination_dir, project_dir_name, data_filename)
            print("data_filepath:", data_filepath)

            self._sess.headers.update({"Referer": f"{DOMAIN}/api/v1/{post["service"]}/user/{post["user"]}/post/{post["id"]}"})

            data_url: str = f"{DOMAIN}/data/{attachment["path"]}"
            print("data_url:", data_url)
            data_reponse: Response = self._sess.get(data_url)

            args_output.write_binary(data_filepath, data_reponse.content)

        # ---- get metadata. ---- #

        # metadata wanted.
        if self._args.need_metadata:
            print("gathering metadata..." + project_dir_name)

            record_filepath: str = path.join(self._destination_dir, project_dir_name, project_dir_name)
            print("record_filepath:", record_filepath)

            meta: dict = {
                Strings.TITLE: post["title"],
                Strings.AUTHOR: creator["name"],
                Strings.DESCRIPTION: post["content"][len("<p>"):-len("</p>")],
                Strings.PUBLISHED: post_time.year,
                Strings.TAGS: post["tags"].strip("{'}").split(),
                Strings.EXTRA: {
                    Strings.FULL_PUBLISHED: post["published"],
                }
            }

            # add file names if more than 1 associated.
            if len(attachment_filenames) > 1:
                meta.update({Strings.FILES: attachment_filenames})

            # save json format.
            if self._args.json_meta:
                args_output.write_json(self._args.allow_overwrite_meta, record_filepath, meta)

            # save toml format.
            if self._args.toml_meta:
                args_output.write_toml(self._args.allow_overwrite_meta, record_filepath, meta)


    def _parse_path_parts(self, url: str) -> list:
        url_parts: ParseResult = urlparse(url)

        path_parts: str = url_parts.path
        path_parts: str = path_parts.strip('/')
        path_parts: list = path_parts.split('/')
        #print("path_parts", path_parts)

        return path_parts


    def _retrieve_profile(self, service: str, creator_id: str) -> dict:
        profile_url: str = f"{DOMAIN}/api/v1/{service}/user/{creator_id}/profile"
        profile_response: Response = self._sess.get(profile_url)
        profile: dict = profile_response.json()
        #print("profile:", profile)

        return profile


    def _retrieve_post(self, service: str, creator_id: str, post_id: str) -> dict:
        post_url: str = f"{DOMAIN}/api/v1/{service}/user/{creator_id}/post/{post_id}"
        post_response: Response = self._sess.get(post_url)
        post: dict = post_response.json()
        print("post:", post)

        return post


def run(args: list):
    scraper: Kemono = Kemono()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
