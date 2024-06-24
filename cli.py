# stdlib.
from argparse import ArgumentParser, Namespace
from os.path import dirname
from sys import argv, exit


class _MODES:
    EDIT_CONFIG: str = "edit-config"
    AUTO_SET: str = "autolist-set"
    AUTO_RUN: str = "autolist-run"
    CMD: str = "cmd"


class _COMMANDS:
    EXIT: str = "exit"
    AUTOLIST: str = "autolist"
    SCRATCH: str = "scratch"


_CONFIG_FILEPATH: str = dirname(__file__) + "/"


def _parse_args(args: list) -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    modes = parser.add_subparsers(dest="mode")

    return parser.parse_args(args)


def _process_edit_config():
    pass


def _process_auto_set():
    pass


def _process_auto_run():
    pass


def _process_cmd():
    pass


def _build_cmd_parser() -> ArgumentParser:
    parser: ArgumentParser = ArgumentParser(add_help=False)
    commands = parser.add_subparsers(dest="command")

    # ---- exit cmd. ---- #

    exit_cmd: ArgumentParser = commands.add_parser(
        _COMMANDS.EXIT,
        add_help=False
    )

    return parser


if __name__ == "__main__":
    args: Namespace = _parse_args(argv[1:])

    # delegate to required mode.
    if args.mode == _MODES.EDIT_CONFIG: _process_edit_config()
    elif args.mode == _MODES.AUTO_SET:  _process_auto_set()
    elif args.mode == _MODES.AUTO_RUN:  _process_auto_run()
    elif args.mode == _MODES.CMD:       _process_cmd()

    # command loop

    exit(0)





























    # ---- autolist cmd. ---- #

    autolist_cmd: ArgumentParser = commands.add_parser(
        _COMMANDS.AUTOLIST,
        help="set the filepath to record scratch commands into",
        add_help=False
    )

    # ---- edit-cfg cmd. ---- #

    edit_cfg_cmd: ArgumentParser = commands.add_parser(
        _COMMANDS.EDIT_CONFIG,
        help="edit the configuration file",
        add_help=False
    )

    # ---- scratch cmd. ---- #

    scratch_cmd: ArgumentParser = commands.add_parser(
        _COMMANDS.SCRATCH,
        help="scrape one or more urls",
        add_help=False
    )
    scratch_cmds = scratch_cmd.add_subparsers(dest="scratch_cmd")

    scratch_cmd.add_argument(
        "--record",
        action="store_true",
        help="record the command in the autolist"
    )

    scratch_cmd.add_argument(
        "--generic",
        action="store_true",
        help="use the generic html scraper"
    )

    scratch_cmd.add_argument(
        "-e",
        nargs="+",
        choices=_gather_scratches(),
        required=False,
        help="use a certain scraper explicitly",
        dest="explicit"
    )

    scratch_cmd.add_argument(
        "urls",
        nargs="+",
        help="one or more urls to scrape"
    )

    # ---- scratch::list. ---- #

    scratch_cmd_list: ArgumentParser = scratch_cmds.add_parser(
        "list",
        help="print a list of scrapers",
        add_help=False
    )

    # ---- scratch::help. ---- #

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




def _process_cmd_mode():
    parser: ArgumentParser = _build_cmd_parser()

    while True:
        cmd: list = input("cmd:").split()
        parsed: Namespace = parser.parse_args(cmd)
        #print("input:", parsed)

        # delegate to required mode.
        if parsed.command == _COMMANDS.EXIT:
            break

        elif parsed.command == _COMMANDS.AUTOLIST:       _process_autolist_command()
        elif parsed.command == _COMMANDS.EDIT_CONFIG:    _process_edit_config_command()
        elif parsed.command == _COMMANDS.SCRATCH:        _process_scratch_command()


def _parse_args(args: list) -> Namespace:
    cmd_mode = modes.add_parser(_MODES.CMD)

    auto_mode = modes.add_parser(_MODES.AUTO)
    auto_mode.add_argument("path", help="filepath to an autolist")
