"""
CURRENT KNOWN ISSUES:
- cannot rip 3d models. browser hook required to infiltrate opengl/vulkan buffers.
"""

# scabies.
from scabies import args_cookies, args_login, args_output, args_time, Strings
from scabies.scraper import Scraper
from scabies.switchplate import SwitchPlate

# scraping.
import yt_dlp
from requests import Response
from urllib.parse import parse_qs, ParseResult, urlparse

# stdlib.
import random, string
from argparse import ArgumentParser
from datetime import datetime
from os import path


NAME: str = "artstation"
DOMAIN: str = "https://www.artstation.com"


class Artstation(Scraper):
    _ALPHABET: str = string.digits + string.ascii_letters
    _BASE: int = len(_ALPHABET)

    class MODES:
        SEARCH: str = "search"
        USER: str = "user"
        PROJECT: str = "project"
        CHALLENGE: str = "challenge"
        LEARNING: str = "learning"

    USER_PARTS: SwitchPlate = SwitchPlate({
        "PORTFOLIO": "P",
        "LIKES": "Li",
        "FOLLOWING": "Fg",
        "FOLLOWERS": "Fr",
        "CHALLENGES": "C",
        "LEARNING": "Lr"
    }, default="P")

    PROJECT_TYPES: SwitchPlate = SwitchPlate({
        "IMAGE": "I",
        "VIDEO": "V"
    }, default="IV")

    PROJECT_PARTS: SwitchPlate = SwitchPlate({
        "MAIN": "M",
        "TAGS": "T",
        "DESC": "Ds",  # description.
        "DATE": "Dt",
        "COMMENTS": "C",
        "STATISTICS": "S"
    }, default="MTDsDtCS")

    _logged_in: bool = False


    def __init__(self):
        super().__init__(NAME)


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self.name()))

        self._parse_args(args)

        # login if desired.
        if self._args.need_login: self._login()

        # delegate to required mode.
        if self._args.mode == self.MODES.SEARCH:       self._process_search_mode()
        elif self._args.mode == self.MODES.USER:       self._process_user_mode()
        elif self._args.mode == self.MODES.PROJECT:    self._process_project_mode()
        elif self._args.mode == self.MODES.CHALLENGE:  self._process_challenge_mode()
        elif self._args.mode == self.MODES.LEARNING:   self._process_learning_mode()

        print(Strings.OP_FINISHED.format(NAME))


    def _parse_args(self, args: list):
        parser: ArgumentParser = ArgumentParser(description="scabies for artstation")
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

        self._add_project_types(search_mode)
        self._add_project_parts(search_mode)

        search_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("search urls")
        )

        # ---- user mode. ---- #

        user_mode: ArgumentParser = modes.add_parser(self.MODES.USER)

        args_time.add_time_selection_args(user_mode)

        self._add_user_parts(user_mode)
        self._add_project_types(user_mode)
        self._add_project_parts(user_mode)

        user_mode.add_argument(
            "names",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("user names")
        )

        # ---- project mode. ---- #

        project_mode: ArgumentParser = modes.add_parser(self.MODES.PROJECT)

        self._add_project_types(project_mode)
        self._add_project_parts(project_mode)

        project_mode.add_argument(
            "projects",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("project ids")
        )

        # ---- challenge mode. ---- #

        challenge_mode: ArgumentParser = modes.add_parser(self.MODES.CHALLENGE)

        args_time.add_time_selection_args(challenge_mode)

        self._add_project_types(challenge_mode)
        self._add_project_parts(challenge_mode)

        challenge_mode.add_argument(
            "positional",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("challenge urls")
        )

        # ---- learning mode. ---- #

        learning_mode: ArgumentParser = modes.add_parser(self.MODES.LEARNING)

        args_time.add_time_selection_args(learning_mode)

        learning_mode.add_argument(
            "urls",
            nargs="+",
            help=Strings.SEQ_SEP_SPACE.format("learning urls")
        )

        # ---- parse and validate. ---- #

        self._args = parser.parse_args()
        #print(f"input: {self._args}")

        # unstructured output wanted.
        if self._args.output_unstructured:
            self._destination_dir = self._args.output_unstructured

        args_output.validate_metadata_args(self._args)

        args_cookies.validate_cookie_args(self._args, self._sess)
        args_login.validate_login_args(self._args)

        args_time.validate_time_selection_args(self._args)


    def _add_user_parts(self, parser: ArgumentParser):
        parser.add_argument(
            "-up",
            default=self.USER_PARTS.default(),
            help=Strings.SEQ_STR_COMBO.format(self.USER_PARTS.legend()),
            dest="user_parts"
        )


    def _add_project_types(self, parser: ArgumentParser):
        parser.add_argument(
            "-pt",
            default=self.PROJECT_TYPES.default(),
            help=Strings.SEQ_STR_COMBO.format(self.PROJECT_TYPES.legend()),
            dest="project_types"
        )


    def _add_project_parts(self, parser: ArgumentParser):
        parser.add_argument(
            "-pp",
            default=self.PROJECT_PARTS.default(),
            help=Strings.SEQ_STR_COMBO.format(self.PROJECT_PARTS.legend()),
            dest="project_parts"
        )


    def _login(self):
        login_url: str = f"{DOMAIN}/api/v2/authentication/session/login.json"

        data: dict = {
            "form_type": "modal",
            "email": self._args.u,
            "password": self._args.p,
            "captcha_token": "",
            "captcha_session_id": "",
            "captcha_public_ip": ""
        }

        headers: dict = {
            "Accept": "*/*",
            "Origin": DOMAIN,
            "Referer": DOMAIN + "/"
        }

        headers.update(self._get_csrf_token())

        login_response: Response = self._sess.post(
            login_url,
            data,
            headers= headers
        )
        print(login_response)


    def _ensure_login(self) -> bool:
        # ensure login.
        if not self._logged_in:
            print("cannot scrape learning without logging in.")

        return self._logged_in


    def _process_search_mode(self):
        for url in self._args.urls:
            parsed: ParseResult = urlparse(url)
            query_items: dict = parse_qs(parsed.query)

            print(query_items)

            print(Strings.SEARCH_STARTED.format())

            # structured output wanted.
            if self._args.output_structured:
                pass
                #self._destination_dir = path.join(self._args.output_structured, NAME, name)

            # need to read time resume file.
            if self._args.need_time_resume:
                pass
                #self._resume_file = path.join(self._destination_dir, time.resume_filename(name))
                #self._resume = time.read_time_resume(self._resume_file)

            """
            params: dict = {
                "query": " ".join(self._args["positional"]),
                "per_page": 50,
                "sorting": "relevance",
                "pro_first": "0",
                "filters": [],
                "additional_fields": ()
            }

            query_url: str = DOMAIN + "/api/v2/search/projects.json"

            # need to read time resume file.
            if self._args.need_time_resume:
                self._resume_file = path.join(self._destination_dir, time.resume_filename(params["query"]))
                self._resume = time.read_time_resume(self._resume_file)

            for data in self._retrieve_paginated(query_url, params=params, as_json=True):
                pass

            # need to write time resume file.
            if self._args.need_time_resume:
                time.write_time_resume(self._resume_filepath)
            """
            print(Strings.SEARCH_FINISHED.format())


    def _process_user_mode(self):
        for name in self._args.names:
            print(Strings.USER_STARTED.format(name))

            # structured output wanted.
            if self._args.output_structured:
                self._destination_dir = path.join(self._args.output_structured, NAME, name)

            # need to read time resume file.
            if self._args.need_time_resume:
                self._resume_file = path.join(self._destination_dir, args_time.resume_filename(name))
                self._resume = args_time.read_time_resume(self._resume_file)

            # portfolio wanted.
            if self.USER_PARTS.CODES.PORTFOLIO in self._args.user_parts:
                print(f"trying to get portfolio from {name}")

                for data in self._retrieve_paginated(DOMAIN + f"/users/{name}/projects.json"):
                    for project_info in data:
                        project: dict = self._retrieve_project(project_info["hash_id"])
                        self._scrape_project(project)

            # likes wanted.
            if self.USER_PARTS.CODES.LIKES in self._args.user_parts:
                print(f"trying to get likes from {name}")

                for data in self._retrieve_paginated(DOMAIN + f"/users/{name}/likes.json"):
                    print(data)
                    #for like_info in data:
                        #project: dict = self._retrieve_project(like_info["hash_id"])
                        #self._scrape_project(project)

            # following wanted.
            if self.USER_PARTS.CODES.FOLLOWING in self._args.user_parts:
                print(f"trying to get following from {name}")

                following_list_filepath: str = path.join(self._destination_dir, "following.txt")
                following_list = open(following_list_filepath, "a")

                for data in self._retrieve_paginated(DOMAIN + f"/users/{name}/following.json"):
                    for following in data:
                        print("found following: {}".format(following["username"]))
                        following_list.write(following["username"])

                following_list.close()

            # followers wanted.
            if self.USER_PARTS.CODES.FOLLOWERS in self._args.user_parts:
                print(f"trying to get followers from {name}")

                followers_list_filepath: str = path.join(self._destination_dir, "followers.txt")
                followers_list = open(followers_list_filepath, "a")

                for data in self._retrieve_paginated(DOMAIN + f"/users/{name}/followers.json"):
                    for follower in data:
                        print("found follower: {}".format(follower["username"]))
                        followers_list.write(follower["username"])

                followers_list.close()

            # challenges wanted.
            if self.USER_PARTS.CODES.CHALLENGES in self._args.user_parts:
                print(f"trying to get challenges from {name}")

                challenges_url: str = DOMAIN + f"/contests/_/challenges/{name}.json"

            # learning wanted.
            if self.USER_PARTS.CODES.LEARNING in self._args.user_parts:
                # proceed only if not logged in.
                if self._ensure_login():
                    print(f"trying to get learning from {name}")

                    user_url: str = f"{DOMAIN}/users/{name}.json"
                    user_response: Response = self._sess.get(user_url)
                    user_json = user_response.json()

                    params: dict = {
                        "per_page": 24,
                        "user_id": user_json["id"]
                    }

                    learning_url: str = DOMAIN + f"/api/v2/learning/courses/instructor_courses_by_user.json"

                    for course in self._retrieve_paginated(learning_url, params=params):
                        self._scrape_learning(course)

            # need to write time resume file.
            if self._args.need_time_resume:
                args_time.write_time_resume(self._resume_filepath)

            print(Strings.USER_FINISHED.format(name))


    def _process_project_mode(self):
        for hash_id in self._args.projects:
            print(f"started project: {hash_id}")

            project: dict = self._retrieve_project(hash_id)
            self._scrape_project(project)

            print(f"finished project: {hash_id}")


    def _process_challenge_mode(self):
        for url in self._args.urls:
            pass


    def _process_learning_mode(self):
        # proceed only if not logged in.
        if self._ensure_login():
            for url in self._args.urls:
                print("started learning: " + url)

                courses: list = []

                # url is a course page.
                if url.startswith(f"{DOMAIN}/learning/courses"):
                    course_response: Response = self._sess.get(url)

                # url is a result gallery.
                elif url.startswith(f"{DOMAIN}/learning"):
                    params: dict = {
                        "per_page": 50,
                        "sort": "latest"
                    }

                    courses: list = self._retrieve_paginated(
                        DOMAIN + "/api/v2/learning/series/search.json",
                        url,
                        params,
                        True
                    )

                    for course in courses:
                        print("found course: " + course["title"])
                        self._scrape_learning(course)

                print("finished learning: " + url)


    def _scrape_project(self, data: dict):
        project_name: str = data["title"]
        post_time: datetime = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")

        # ---- time cutoff. ---- #

        # skip for time resume.
        if self._args.need_time_resume and post_time <= self._resume_time:
            print(Strings.SKIP_TIME_RESUME)
            return

        # skip for time cutoff.
        if self._args.need_time_cutoff and args_time.exceeds_time_cutoff_limits(self._args, post_time):
            print(Strings.SKIP_TIME_CUTOFF)
            return

        # ---- collect data. ---- #

        project_dir_name: str = str(data["id"]) + '_' + data["slug"]
        asset_filenames: list = []

        for asset in data["assets"]:
            # cover image.
            if (
                asset["asset_type"] == "cover" and
                self.PROJECT_TYPES.CODES.IMAGE in self._args.project_types
            ):
                print("found cover image")

            # image.
            if (
                asset["asset_type"] == "image" and
                self.PROJECT_TYPES.CODES.IMAGE in self._args.project_types
            ):
                print("found image")

                username: str = data["user"]["username"]
                image_url = asset["image_url"]

                image_filename: str = image_url.split("?")[0]
                image_filename = path.basename(image_filename)

                image_filepath: str = path.join(self._destination_dir, project_dir_name, image_filename)
                print("image_filepath:", image_filepath)

                # metadata wanted.
                if self._args.need_metadata:
                    asset_filenames.append(image_filename)

                image_data = self._pull_image(asset)
                args_output.write_binary(image_filepath, image_data)

            # video.
            elif (
                asset["asset_type"] == "video" and
                self.PROJECT_TYPES.CODES.VIDEO in self._args.project_types
            ):
                print("found video")

                video_filename: str = ""

                # metadata wanted.
                if self._args.need_metadata:
                    asset_filenames.append(video_filename)

                self._pull_video(asset)

            # video clip.
            elif (
                asset["asset_type"] == "video_clip" and
                self.PROJECT_TYPES.CODES.VIDEO in self._args.project_types
            ):
                print("found video clip")

            # marmoset 3d model.
            elif (
                asset["asset_type"] == "marmoset" and
                self.PROJECT_TYPES.CODES.MODEL in self._args.project_types
            ):
                # todo: find an open source alt of ninjaripper.
                pass

            # model3d.
            elif (
                asset["asset_type"] == "model3d" and
                self.PROJECT_TYPES.CODES.MODEL in self._args.project_types
            ):
                # todo: find and open source alt of ninjaripper.
                pass

        # ---- get metadata. ---- #

        # metadata wanted.
        if self._args.need_metadata:
            print("gathering metadata..." + project_dir_name)

            record_filepath: str = path.join(self._destination_dir, project_dir_name, project_dir_name)

            meta: dict = {
                Strings.TITLE: project_name,
                Strings.AUTHOR: data["user"]["username"],
                Strings.DESCRIPTION: data["description"][len("<p>"):-len("</p>")],
                Strings.PUBLISHED: post_time,
                Strings.TAGS: [tag.lower() for tag in data["tags"]],
                Strings.EXTRA: {
                    Strings.FULL_PUBLISHED: data["created_at"],
                    "software": [ware["name"] for ware in data["software_items"]]
                }
            }

            # add file names if more than 1 associated.
            if len(asset_filenames) > 1:
                meta.update({Strings.FILES: asset_filenames})

            # save json format.
            if self._args.json_meta:
                args_output.write_json(self._args.allow_overwrite_meta, record_filepath, meta)

            # save toml format.
            if self._args.toml_meta:
                args_output.write_toml(self._args.allow_overwrite_meta, record_filepath, meta)


    def _scrape_likes(self, data: dict):
        pass


    def _scrape_challenge(self, data: dict):
        pass


    def _scrape_learning(self, data: dict):
        print(data)
        print("found course: " + data["title"])

        hash_id: str = data["hash_id"]
        slug: str = data["slug"]

        course_url: str = f"{DOMAIN}/learning/{hash_id}/{slug}/"
        course_response: Response = self._sess.get(course_url)

        print(course_response.content)


    def _retrieve_paginated(self, url: str, ref: str= "", params: dict= {}, as_json: bool= False) -> list:
        print("started paginating:", url)

        # NOTE:
        # starts as a GET method by default. if the GET is for a json document,
        # the presence of secondary json parameters will be used to signal below
        # to change the method to POST.

        # the call automatically starts from the first page and acquires additional
        # pages in the while loop toward the end.

        method: str = "GET"

        headers: dict = {
            "Accept": "application/json, text/plain, */*",
            "Origin": DOMAIN
        }

        # header needs referer.
        if ref: headers.update({"Referer": ref})
        else:   headers.update({"Referer": f"{DOMAIN}/"})

        # NOTE: pagination must always start at page 1.
        params.update({"page": 1})

        # need secondary json setup.
        if as_json:
            method = "POST"
            headers.update(self._get_csrf_token())

        # ---- retrieval loop. ---- #

        req_params: dict = None if as_json else params
        json_params: dict = params if as_json else None

        acquired: int = 0

        while True:
            page_response: Response = self._sess.request(
                method,
                url,
                req_params,
                headers=headers,
                json=json_params
            )
            #print(page_response)

            print(page_response.text)

            page: dict = page_response.json()
            import json
            json.loads(page_response.text)
            #print("page:", page)

            yield page["data"]

            acquired += len(page["data"])
            params["page"] += 1

            # break out when all items are acquired.
            if acquired == page["total_count"]:
                break

        print("finished paginating:", url)


    def _get_csrf_token(self):
        token_response: Response = self._sess.post(
            DOMAIN + "/api/v2/csrf_protection/token.json",
            json={},
            headers={
                "Accept": "*/*",
                "Origin": DOMAIN,
                "Referer": DOMAIN + "/",
            }
        )
        token: dict = token_response.json()

        return {"PUBLIC-CSRF-TOKEN": token["public_csrf_token"]}


    def _retrieve_project(self, hash_id: str) -> dict:
        project_url: str = DOMAIN + "/projects/" + hash_id + ".json"
        project_response: Response = self._sess.get(project_url)
        project: dict = project_response.json()

        # structured output wanted.
        if self._args.output_structured:
            self._destination_dir = path.join(self._args.output_structured, NAME, project["user"]["username"])

        return project


    def _pull_image(self, asset: dict):
        # ---- prepare the imagedata url. ---- #

        # note: useless whiffer parameter added to cause a cache miss
        # in cloudflare, otherwise it will destroy the quality if any images
        # sent through.

        whiffer_url: str = asset["image_url"]

        # query parameter already present in url.
        if "?" in whiffer_url:
            whiffer_url += "&"
        else:
            whiffer_url += "?"

        whiffer_url += "whiffer="

        counter: int = random.getrandbits(64)
        encoded: str = ""

        while counter:
            remainder = counter % self._BASE
            counter = counter // self._BASE
            encoded = self._ALPHABET[remainder] + encoded

        whiffer_url += encoded

        hd_parts: tuple = whiffer_url.partition("/large/")
        hd_url: str = hd_parts[0] + "/4k/" + hd_parts[1]

        # ---- get imagedata. ---- #

        image_response: Response = self._sess.get(hd_url)

        # hd get failed.
        if image_response.status_code != 200:
            image_response = self._sess.get(whiffer_url)

        return image_response.content


    def _pull_video(self, asset: dict):
        video_url: str = asset[""]


def run(args: list):
    scraper: Artstation = Artstation()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
