# stdlib.
from argparse import ArgumentParser, Namespace
from importlib import import_module
from os import listdir, path
from sys import argv, exit
from types import ModuleType


class MODES:
    COMMAND: str = "cmd"
    AUTOMATE: str = "auto"


class CMDS:
    EXIT: str = "exit"
    EDIT_CONFIG: str = "edit-config"
    AUTOLIST: str = "autolist"


def _parse_args(args: list) -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    modes = parser.add_subparsers(
        title="modes",
        dest="mode",
        required=True,
        help="see individual mode helps for details"
    )

    # ---- modes. ---- #

    command_mode: ArgumentParser = modes.add_parser(MODES.COMMAND)

    automate_mode: ArgumentParser = modes.add_parser(MODES.AUTOMATE)

    # ---- results. ---- #

    return parser.parse_args(args)


def _process_cmd_mode():
    while True:
        cmd: Namespace = _parse_cmd(input("cmd:").split())

        # exit.
        if cmd.cmd == CMDS.EXIT:
            break

        # edit config file.
        elif cmd.cmd == CMDS.EDIT_CONFIG:
            pass

        # set autolist file.
        elif cmd.cmd == CMDS.AUTOLIST:
            pass


def _process_auto_mode():
    pass


def _gather_scratches() -> list:
    scratch_path: str = path.join(path.dirname(__file__), "scratches")
    scratch_prefixes: list = ["meta_", "neo_"]
    scratches: list = []

    for found in listdir(scratch_path):
        for prefix in scratch_prefixes:
            # found a scratch.
            if found.startswith(prefix):
                scratch: ModuleType = import_module(f"scratches.{path.splitext(found)[0]}")
                print(scratch.NAME)

    return scratches


def _parse_cmd(args: list) -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    commands = parser.add_subparsers(
        title="commands",
        dest="cmd",
        required=True,
        help="see individual command helps for details"
    )

    # ---- exit. ---- #

    commands.add_parser(
        CMDS.EXIT,
        help="exit the program"
    )

    # ---- edit. ---- #

    commands.add_parser(
        CMDS.EDIT_CONFIG,
        help="edit the config file in an interactive interface"
    )

    # ---- autolist. ---- #

    commands.add_parser(
        CMDS.AUTOLIST,
        help="specify an automation list to put any recorded commands in"
    )

    # ---- results. ---- #

    return parser.parse_args(args)


if __name__ == "__main__":
    args: Namespace = _parse_args(argv[1:])

    # delegate to required mode.
    if args.mode == MODES.COMMAND:       _process_cmd_mode()
    elif args.mode == MODES.AUTOMATE:    _process_auto_mode()

    exit(0)








"""
# stdlib.
from collections import namedtuple



from urllib.parse import urlparse, ParseResult


class ModInfo:
    def __init__(self, name: str, domains: list, run):
        self._name: str = name
        self._domains: list = domains
        self._run = run


    def name(self) -> str:
        return self._name

    name.__doc__ = ""


    def can_handle(self, domain: str) -> bool:
        return domain in self._domains

    can_handle.__doc__ = ""


    def run(self, args: list):
        self._run(args)

    run.__doc__ = ""





def _parse_cmd():
    # ---- scratch command. ---- #

    scratch_command = commands.add_parser(
        "scratch",
        help="try scraping one or more urls"
    )

    scratch_command.add_argument(
        "--generic",
        action="store_true",
        help="use the generic scraper"
    )

    scratch_command.add_argument(
        "--add-to-auto",
        action="store_true",
        help="add successful scraped urls to an autolist"
    )

    scratch_command.add_argument(
        "urls",
        nargs="+",
        help="list of urls to scrape"
    )







def _process_cmd_mode():
    modules: list = _gather_modules()
    cmd_running: bool = True

    print("Hint: Enter -h as a command to get help text.")

    while cmd_running:
        cmd: str = input("cmd:")
        args: Namespace = _parse_cmd(cmd)

        # exit.
        if args.cmd == "exit":
            cmd_running = False

        # edit.
        elif args.cmd == "edit-config":
            

            

        # autolist.
        elif args.cmd == "autolist":
            pass

        # scratch.
        elif args.cmd == "scratch":
            for url in args.urls:
                url_parts: ParseResult = urlparse(url)

                handler: ModInfo | None = None

                for module in modules:
                    # module can handle the domain.
                    if module.can_handle(url_parts.netloc):
                        handler = module

                # user wants to scrape generic webpages.
                if args.generic:
                    for module in modules:
                        # generic module.
                        if module.name() == "generic":
                            print("DEV: finish implementing: run generic scraper")

                # modules has a matching scraper.
                elif handler:
                    print("DEV: finish implementing: run matching scraper")

                # no suitable scraper found.
                else:
                    print("No suitable scraper was found for urls at " + url_parts.netloc)

"""
