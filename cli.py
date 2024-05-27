# entry point.
if __name__ == "__main__":
    # stdlib.
    from argparse import ArgumentParser, Namespace
    from importlib import import_module
    from os import path, listdir
    from sys import argv, exit
    from types import ModuleType


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

        # ---- edit. ---- #

        edit_config_cmd = commands.add_parser(
            COMMANDS.EDIT_CONFIG,
            help="edit the config file in an interactive interface"
        )

        # ---- scratch. ---- #

        scratch_cmd = commands.add_parser(
            COMMANDS.SCRATCH,
            help="try scraping one or more urls"
        )

        scrape_parser.add_argument("--record", action="store_true", help="Record the scraping process")
        scrape_parser.add_argument("--generic", action="store_true", help="Use generic mode for scraping")
        scrape_parser.add_argument("urls", nargs="*", help="One or more URLs to scrape")

        scratch_subparsers = scratch_cmd.add_subparsers(dest="cmd", required=True)

        list_parser = scratch_subparsers.add_parser("list", help="List resources")

        help_parser = scratch_subparsers.add_parser("help", help="Show help for a specific name")
        help_parser.add_argument("name", nargs='?', help="The name to provide help for")

        # ---- autolist. ---- #

        autolist_cmd = commands.add_parser(
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


    def _gather_scratches() -> list:
        scratch_path: str = path.join(path.dirname(__file__), "scratches")
        scratch_prefix: str = "neo_"

        scratches: list = []

        for found in listdir(scratch_path):
            # found a scratch.
            if found.startswith(scratch_prefix):
                scratch: ModuleType = import_module(f"scratches.{path.splitext(found)[0]}")
                print(scratch.NAME)

        return scratches


    args: Namespace = _parse_args(argv[1:])

    # delegate to required mode.
    if args.command == COMMANDS.EDIT_CONFIG:    pass
    elif args.command == COMMANDS.SCRATCH:      pass
    elif args.command == COMMANDS.AUTOLIST:     pass

    exit(0)













    scrape_parser = scratch_subparsers.add_parser("scrape", help="Scrape URLs with optional flags")


    while True:
        print("hint: enter -h or --help as a command to get help text.")

        cmd: Namespace = (input("cmd:").split())
