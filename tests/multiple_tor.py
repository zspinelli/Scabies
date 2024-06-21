# stdlib.
import atexit
import re
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count
from os import path, environ
from platform import system
from subprocess import Popen

# test.
import requests
from requests import Response
from stem import process, Signal
from stem.control import Controller


_OS_TOR_PATH: dict = {
    "Windows": path.join(environ["USERPROFILE"], "Desktop", "Tor Browser", "Browser", "TorBrowser", "Tor", "tor.exe")
    # "Linux": path.join()
    # "Darwin": path.join()
}


_tor_path: str = _OS_TOR_PATH[system()]
_tor_proc: Popen | None = None


def _callback(line: str):
    # new bootstrap status update.
    if "Bootstrapped" in line:
        print(line)


def _stop():
    global _tor_proc

    # tor is running.
    if _tor_proc:
        print("stopping tor...")
        _tor_proc.kill()
        _tor_proc = None


def _task():
    with requests.Session() as session:
        session.proxies = {
            "http": "socks5h://localhost:9150",
            "https": "socks5h://localhost:9150"
        }

        with Controller.from_port(port=9150) as controller:
            print("created controller")

            controller.authenticate()
            print("authenticated controller")

            controller.signal(Signal.NEWNYM)

            response: Response = session.get("http://httpbin.org/ip")
            print(response.text)


if __name__ == "__main__":
    pool = ProcessPoolExecutor()

    atexit.register(_stop)

    _tor_proc = process.launch_tor_with_config(
        config={"SocksPort": "9150"},
        init_msg_handler=_callback,
        tor_cmd=_tor_path
    )

    for i in range(cpu_count()):
        pool.submit(_task)

    pool.shutdown(wait=True)
