# stdlib.
from abc import ABC, abstractmethod
from argparse import Namespace
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from importlib import import_module
from multiprocessing import cpu_count
from os import path, listdir
from types import ModuleType

# scabies.
from scabies import session, Strings
from scabies.session import ScabiesSession


class ScraperInfo:
    def __init__(self, name: str, domain: str, modes: list, particles: dict):
        self.NAME = name
        self.DOMAIN = domain
        self.MODE = None

        # ---- modes. ---- #

        for mode in modes:
            setattr(self.MODE, mode.upper(), mode.lower())

        # ---- particles. ---- #

        for key, value in particles:
            default: list = []
            legend: list = []

            setattr(self, key.upper(), None)
            attr = getattr(self, key.upper())

            for name, code in value:
                pass

            setattr(attr, "LEGEND", default)
            setattr(attr, "DEFAULT", legend)


_scratches: list = []


class Scraper(ABC):
    __doc__ = "base class for all scrapers. features name(), run(), and _parse_args() to " \
        "assist automation by the umbrella cli."

    def __init__(self, name: str, domain: str, interval: int = 0):
        self._name: str = name
        self._domain: str = domain

        self._args: Namespace = Namespace()
        self._sess: ScabiesSession = session.new(interval)

        self._destination_dir: str = ""
        self._resume_filepath: str = ""
        self._resume_time: datetime = datetime.min


    @abstractmethod
    def _parse_args(self, args: list):
        pass

    _parse_args.__doc__ = "parse the parameters: list[str] passed from self.run()"


    @abstractmethod
    def run(self, args: list):
        pass

    run.__doc__ = "run the scraper on parameters: list[str] passed to args"


    def auto_resolve(self, url: str, outpath: str):
        pass


class MetaScraper(Scraper):
    def __init__(self, name, domain, thread_task, print_stats):
        super().__init__(name, domain)

        self._sess = None

        self._slots: list = []
        self._num_slots: int = cpu_count() * 2
        self._pool: ProcessPoolExecutor = ProcessPoolExecutor(self._num_slots)

        self._thread_task = thread_task
        self._print_stats = print_stats


    def run(self, args: list):
        print(Strings.OP_STARTING.format(self._name))

        self._parse_args(args)

        self._resume_filepath: str = f"{self._args.output}/{self._name}_resume.txt"

        with ProcessPoolExecutor(cpu_count() + 1) as self._pool:
            self._pool.submit(self._main_task)

            while True:
                # user requests early exit.
                if input("type \"q\" to stop:") in ["q", "Q"]:
                    break

        print(Strings.OP_FINISHED.format(self._name))


    def _main_task(self):
        for slot in self._slots:
            self._pool.submit(self._thread_task, slot)


def gather_scratches() -> list:
    scratch_path: str = path.join(path.dirname(__file__), "scratches")
    scratches: list = []

    for found in listdir(scratch_path):
        module: ModuleType = import_module(f"scratches.{path.splitext(found)[0]}")

        scratch: _Scratch = _Scratch(

        )
        scratches.append(scratch)

    return scratches
