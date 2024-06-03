# entry point.
if __name__ == "__main__":
    # stdlib.
    from argparse import ArgumentParser, Namespace
    from importlib import import_module
    from os import path, listdir
    from sys import argv, exit
    from types import ModuleType


    class MODES:
        CMD: str = "cmd"
        AUTO: str = "auto"

    class COMMANDS:
        EXIT: str = "exit"
        AUTOLIST: str = "autolist"
        EDIT_CONFIG: str = "edit-config"
        SCRATCH: str = "scratch"


    CONFIG_FILEPATH: str = ""


    def gather_scratches() -> list:
        scratch_path: str = path.join(path.dirname(__file__), "scratches")
        scratches: list = []

        for found in listdir(scratch_path):
            scratch: ModuleType = import_module(f"scratches.{path.splitext(found)[0]}")
            print(scratch.NAME)

        return scratches


    def build_structure():
        pass


    def build_cmd_parser() -> ArgumentParser:
        parser: ArgumentParser = ArgumentParser(add_help=False)
        commands = parser.add_subparsers(dest="command")

        # ---- exit cmd. ---- #

        exit_cmd: ArgumentParser = commands.add_parser(
            COMMANDS.EXIT,
            add_help=False
        )

        # ---- autolist cmd. ---- #

        autolist_cmd: ArgumentParser = commands.add_parser(
            COMMANDS.AUTOLIST,
            help="set the filepath to record scratch commands into",
            add_help=False
        )

        # ---- edit-cfg cmd. ---- #

        edit_cfg_cmd: ArgumentParser = commands.add_parser(
            COMMANDS.EDIT_CONFIG,
            help="edit the configuration file",
            add_help=False
        )

        # ---- scratch cmd. ---- #

        scratch_cmd: ArgumentParser = commands.add_parser(
            COMMANDS.SCRATCH,
            help="scrape one or more urls",
            add_help=False
        )
        scratch_cmds = scratch_cmd.add_subparsers(dest="scratch_cmd")

        scratch_cmd.add_argument(
            "record",
            action="store_true",
            help="record the command in the autolist"
        )

        scratch_cmd.add_argument(
            "generic",
            action="store_true",
            help="use the generic html scraper"
        )

        scratch_cmd.add_argument(
            "urls",
            nargs="+",
            help="one or more urls to scrape"
        )

        scratch_cmd_help: ArgumentParser = scratch_cmds.add_parser(
            "help",
            help="print usage for a scraper",
            prefix_chars="/",
            add_help=False
        )

        scratch_cmd_help.add_argument(
            "name",
            help="scraper name to provide help for"
        )

        return parser


    def process_autolist_command():
        pass


    def process_edit_config_command():
        pass


    def process_scratch_command():
        pass


    def process_cmd_mode():
        parser: ArgumentParser = build_cmd_parser()
        scratches: list = gather_scratches()

        while True:
            cmd: list = input("cmd:").split()
            parsed: Namespace = parser.parse_args(cmd)
            #print(parsed)

            # delegate to required mode.
            if parsed.command == COMMANDS.EXIT:
                break

            elif parsed.command == COMMANDS.AUTOLIST:       process_autolist_command()
            elif parsed.command == COMMANDS.EDIT_CONFIG:    process_edit_config_command()
            elif parsed.command == COMMANDS.SCRATCH:        process_scratch_command()


    def process_auto_mode(args: Namespace):
        with open(args.path, "r") as autolist:
            pass


    def parse_args(args: list) -> Namespace:
        parser: ArgumentParser = ArgumentParser()
        modes = parser.add_subparsers(dest="mode")

        cmd_mode = modes.add_parser(MODES.CMD)

        auto_mode = modes.add_parser(MODES.AUTO)
        auto_mode.add_argument("path", help="filepath to an autolist")

        return parser.parse_args(args)


    args: Namespace = parse_args(argv[1:])

    # delegate to required mode.
    if args.mode == MODES.CMD:      process_cmd_mode()
    elif args.mode == MODES.AUTO:   process_auto_mode(args)

    exit(0)
