# entry point.
if __name__ == "__main__":
    # stdlib.
    from argparse import ArgumentParser, Namespace
    from sys import argv, exit


    class COMMANDS:
        EDIT_CONFIG: str = "edit-config"
        SCRATCH: str = "scratch"
        AUTOLIST: str = "autolist"


    def _parse_args(args: list) -> Namespace:
        parser: ArgumentParser = ArgumentParser()
        commands = parser.add_subparsers(
            title="commands",
            dest="cmd",
            required=True,
            help="see individual command helps for details"
        )

        commands.add_parser(
            COMMANDS.EDIT_CONFIG,
            help="edit the config file in an interactive interface"
        )

        commands.add_parser(
            COMMANDS.AUTOLIST,
            help="specify an automation list to put any recorded commands in"
        )

        return parser.parse_args(args)


    def _process_edit_config_command():
        pass


    def _process_scratch_command():
        pass


    def _process_auto_command():
        pass


    args: Namespace = _parse_args(argv[1:])

    # delegate to required mode.
    if args.command == COMMANDS.EDIT_CONFIG:    pass
    elif args.command == COMMANDS.SCRATCH:      pass
    elif args.command == COMMANDS.AUTOLIST:     pass

    exit(0)
















# stdlib.

from importlib import import_module
from os import listdir, path

from types import ModuleType


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


def _process_cmd_mode():


    commands.add_parser(CMDS.EXIT, help="exit the program")


    scratch_command = commands.add_parser(CMDS.SCRATCH, help="try scraping one or more urls")
    scratch_subparsers = scratch_command.add_subparsers(dest="command", required=True)

    list_parser = scratch_subparsers.add_parser("list", help="List resources")

    help_parser = scratch_subparsers.add_parser("help", help="Show help for a specific name")
    help_parser.add_argument("name", nargs='?', help="The name to provide help for")

    scrape_parser = scratch_subparsers.add_parser("scrape", help="Scrape URLs with optional flags")
    scrape_parser.add_argument("--record", action="store_true", help="Record the scraping process")
    scrape_parser.add_argument("--generic", action="store_true", help="Use generic mode for scraping")
    scrape_parser.add_argument("urls", nargs="*", help="One or more URLs to scrape")

    while True:
        print("hint: enter -h or --help as a command to get help text.")

        cmd: Namespace = (input("cmd:").split())


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


def _process_cmd_mode():
    modules: list = _gather_modules()
    cmd_running: bool = True


    while cmd_running:
        cmd: str = input("cmd:")
        args: Namespace = _parse_cmd(cmd)

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
