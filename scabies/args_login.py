# stdlib.
from argparse import ArgumentParser, Namespace


def add_login_args(parser: ArgumentParser, id_type: str):
    login_group = parser.add_argument_group("login")

    login_group.add_argument(
        "-u",
        type=str,
        help=f"{id_type} for login"
    )

    login_group.add_argument(
        "-p",
        type=str,
        help="password for login"
    )


def validate_login_args(parsed: Namespace):
    parsed.need_login = hasattr(parsed, "u") or hasattr(parsed, "p")
