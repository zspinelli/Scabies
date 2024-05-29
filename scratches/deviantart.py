# scabies.
from scabies import Strings, session
from scabies.scraper import Scraper
from scabies.switchplate import SwitchPlate


class Deviantart(Scraper):
    class MODES:
        SEARCH: str = "search"
        USER: str = "users"
        FOLDER: str = "folder"
        ART: str = "art"
        POST: str = "post"
        META: str = "meta"

    USER_PARTS: SwitchPlate = SwitchPlate({
        "GALLERY": "G",
        "FAVORITES": "F",
        "POSTS": "P"
    }, default="G")

    ART_TYPES: SwitchPlate = SwitchPlate({
        "IMAGE": "I",
        "WRITING": "W"
    }, default="IW")

    ART_PARTS: SwitchPlate = SwitchPlate({
        "MAIN": "M",
        "TAGS": "T",
        "DESC": "Ds",  # description.
        "DATE": "Dt",
        "COMMENTS": "C",
        "STATISTICS": "S",
        "DOWNLOAD": "Dn"
    }, default="MTDsDtCSDn")


    def __init__(self):
        super().__init__("deviantart", "https://www.deviantart.com")


    def _parse_args(self, args: list):
        pass


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self._name))

        self._sess = session.new()
        self._parse_args(argv)

        # delegate to required mode.
        if self._args.mode == self.MODES.SEARCH:     self._process_search_mode()
        elif self._args.mode == self.MODES.USER:     self._process_user_mode()
        elif self._args.mode == self.MODES.FOLDER:   self._process_folder_mode()
        elif self._args.mode == self.MODES.ART:      self._process_art_mode()

        print(Strings.OP_FINISHED.format(self._name))


def run(args: list):
    scraper: Deviantart = Deviantart()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
