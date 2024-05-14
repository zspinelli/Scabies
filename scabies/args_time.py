# stdlib.
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from os import path
from datetime import datetime


TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def _parse_datetime(p_time):
    try:
        return datetime.strptime(p_time, TIME_FORMAT)

    except ValueError:
        raise ArgumentTypeError("Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS.")


def add_time_selection_args(parser: ArgumentParser):
    time_cutoff_group = parser.add_argument_group("time cutoff")

    after_group = time_cutoff_group.add_mutually_exclusive_group()

    after_group.add_argument(
        "-dca",
        help="ignore posts after a YYYY-MM-DD HH:MM:SS timestamp",
        type=_parse_datetime,
        dest="lower_limit"
    )

    after_group.add_argument(
        "-dcai",
        help="ignore posts on or after a YYYY-MM-DD HH:MM:SS timestamp",
        type=_parse_datetime,
        dest="lower_limit"
    )

    before_group = time_cutoff_group.add_mutually_exclusive_group()

    before_group.add_argument(
        "-dcb",
        help="ignore posts before a YYYY-MM-DD HH:MM:SS timestamp",
        type=_parse_datetime,
        dest="upper_limit"
    )

    before_group.add_argument(
        "-dcbi",
        help="ignore posts on or before YYYY-MM-DD HH:MM:SS timestamp",
        type=_parse_datetime,
        dest="upper_limit"
    )

    time_resume_group = parser.add_argument_group("time resume")

    time_resume_group.add_argument(
        "--lrr",
        action="store_true",
        help="store last run time for resume",
        dest="need_time_resume"
    )


def validate_time_selection_args(parsed: Namespace):
    # need time cutoff.
    parsed.need_time_cutoff = bool(hasattr(parsed, "lower_limit") or hasattr(parsed, "upper_limit"))

    # need time resume.
    if not hasattr(parsed, "need_time_resume"):
        parsed.need_time_resume = False


def exceeds_time_cutoff_limits(parsed: Namespace, date: datetime) -> bool:
    outside: bool = False

    # lower or upper bounds crossed.
    if parsed.lower_limit and date < parsed.lower_limit: return True
    elif parsed.upper_limit and date > parsed.upper_limit: return True

    return False


def resume_filename(name: str) -> str:
    return "{}-time-resume.txt".format(name)


def read_time_resume(filepath: str) -> datetime:
    if path.isfile(filepath):
        with open(filepath, "r") as file:
            return datetime.strptime(file.readline(), TIME_FORMAT)

    return datetime.utcfromtimestamp(0)


def write_time_resume(filepath: str):
    with open(filepath, "w") as file:
        file.write(datetime.today().strftime(TIME_FORMAT))
        print(f"** WROTE TIME RESUME: {filepath} **")
