# entry point.
if __name__ == "__main__":
    # stdlib.
    from importlib import import_module
    from os import path, listdir
    from sys import argv, exit
    from types import ModuleType

    # scabies.
    from scabies.argparser import ArgParser


    class MODES:
        CMD: str = "cmd"
        AUTO: str = "auto"

    class COMMANDS:
        EDIT_CONFIG: str = "edit-config"
        SCRATCH: str = "scratch"
        AUTOLIST: str = "autolist"


    def parse_args(args: list) -> dict:
        parser: ArgParser = ArgParser()

        parser.add_branch(MODES.CMD, dest="mode")
        parser.add_branch(MODES.AUTO, dest="mode")

        return parser.parse(args)


    def process_cmd_mode():
        pass


    def process_auto_mode():
        pass


    def _parse_cmd(args: list) -> dict:
        parser: ArgParser = ArgParser()

        # ---- autolist. ---- #

        autolist_cmd: ArgParser = parser.add_branch("autolist", "cmd")

        # ---- edit cfg. ---- #

        edit_cfg_cmd: ArgParser = parser.add_branch("edit-cfg", "cmd")

        # ---- scratch. ---- #

        scratch_cmd: ArgParser = parser.add_branch("scratch", dest = "cmd", usage = "scrape urls with optional flags")
        scratch_cmd.add_switch("record", False, usage = "record the command in the autolist")
        scratch_cmd .add_switch("generic", False, usage = "use the generic html scraper")
        scratch_cmd.add_remainder("urls", "one or more urls to scrape")

        scratch_cmd.add_branch("list", dest = "scratch_cmd")

        scratch_help_cmd: ArgParser = scratch_cmd.add_branch("help", dest = "scratch_cmd")
        scratch_help_cmd.add_option("name", usage = "scraper name to provide help for")

        return parser.parse(args)


    def _cmd_loop():
        parser: ArgParser = ArgParser()

        while True:
            cmd: list = input("cmd:").split()
            parsed: dict = parser.parse(cmd)

            # --- . ---- #

            # ---- . ---- #

            # ---- scrape command. ---- #


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


    args: dict = _parse_args(argv[1:])
    #args: Namespace = _parse_args(argv[1:])

    # delegate to required mode.
    if args.command == COMMANDS.EDIT_CONFIG:    pass
    elif args.command == COMMANDS.SCRATCH:      pass
    elif args.command == COMMANDS.AUTOLIST:     pass

    exit(0)
