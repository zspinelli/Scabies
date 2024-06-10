"""
CURRENT KNOWN ISSUES:
- sometimes the tor connection will drop.
- the tor interface is not able to use an existing tor connection.
- the tor interface is not able to find tor in other locations.
"""

# stdlib.
import atexit, re
from argparse import ArgumentParser, Namespace
from os import environ, path
from platform import system
from subprocess import Popen

# scraping.
from stem import process


_OS_TOR_PATH: dict = {
    "Windows": path.join(environ["USERPROFILE"], "Desktop", "Tor Browser", "Browser", "TorBrowser", "Tor", "tor.exe")
    # "Linux": path.join()
    # "Darwin": path.join()
}


_tor_path: str = _OS_TOR_PATH[system()]
_tor_proc: Popen | None = None


def add_tor_args(parser: ArgumentParser):
    tor_group = parser.add_argument_group("tor")

    tor_group.add_argument(
        "-tor",
        default=_OS_TOR_PATH[system()],
        required=False,
        help="abs. or rel. path to tor install directory"
    )


def validate_tor_args(parsed: Namespace):
    global _tor_path

    # no tor path was given.
    if not hasattr(parsed, "tor"):
        _tor_path = _OS_TOR_PATH[system()]


def _stop():
    global _tor_proc

    # tor is running.
    if _tor_proc:
        print("stopping tor...")
        _tor_proc.kill()
        _tor_proc = None


def _callback(line: str):
    # new bootstrap status update.
    if re.search("Bootstrapped", line):
        print(line)


def start() -> bool:
    global _tor_proc

    try:
        #print(f"base:\t{_BASE_PATH[os_name]}")
        #print(f"tor:\t{_TOR_PATH[os_name]}\n")

        print("starting tor...")

        _tor_proc = process.launch_tor_with_config(
            config={"SocksPort": "9150"},
            init_msg_handler=_callback,
            tor_cmd=_tor_path
        )

        atexit.register(_stop)
        return True

    except Exception as tor_ex:
        print("tor_ex:", tor_ex)
        return False
