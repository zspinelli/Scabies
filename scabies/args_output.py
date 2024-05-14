# stdlib.
import json
from argparse import ArgumentParser, Namespace
from os import makedirs, path
from os.path import dirname

# scraping.
import tomlkit
from tomlkit import TOMLDocument

# scabies.
from scabies import Strings


def add_output_args(parser: ArgumentParser):
    output_group = parser.add_argument_group("output")

    output_group.add_argument(
        "--ao",
        action="store_false",
        help="allow overwriting existing files. doesn't affect metadata behavior.",
        dest="allow_overwrite"
    )

    output_exclusive = output_group.add_mutually_exclusive_group(required=True)

    output_exclusive.add_argument(
        "-os",
        help="base output path (structured). builds an organized folder tree in the directory if applicable.",
        dest="output_structured"
    )

    output_exclusive.add_argument(
        "-ou",
        help="base output path (unstructured). puts everything into the directory with minimal sorting.",
        dest="output_unstructured"
    )


def validate_output_args(parsed: Namespace):
    # TODO: ensure that -os and -ou point to valid destinations.
    pass


def add_metadata_args(parser: ArgumentParser):
    metadata_group = parser.add_argument_group("metadata")

    metadata_group.add_argument(
        "--aom",
        action="store_false",
        help="allow overwriting existing metadata files.",
        dest="allow_overwrite_meta"
    )

    metadata_group.add_argument(
        "--json-meta",
        action="store_true",
        help="metadata as json"
    )

    metadata_group.add_argument(
        "--toml-meta",
        action="store_true",
        help="metadata as toml"
    )


def validate_metadata_args(parsed: Namespace):
    parsed.need_metadata = parsed.json_meta or parsed.toml_meta


def write_binary(filepath: str, payload):
    makedirs(dirname(filepath), exist_ok=True)

    with open(filepath.encode("utf-8"), "wb") as out:
        out.write(payload)

    print(f"wrote {filepath}")


def write_json(allow_overwrite: bool, filepath: str, data: dict) -> bool:
    filepath = filepath + ".json"

    # prevent file overwrite?
    if not allow_overwrite and path.exists(filepath):
        print(strings.SKIP.format(strings.SKIP_NO_CLOBBER) + '\n')
        return False

    # ---- writing. ---- #

    makedirs(dirname(filepath), exist_ok=True)

    json_filepath: str = filepath
    json_data = json.dumps(data, indent=4)

    with open(json_filepath, "w") as json_record:
        json_record.write(json_data)

    print(f"wrote {json_filepath}")
    return True


def write_toml(allow_overwrite: bool, filepath: str, data: dict) -> bool:
    filepath = filepath + ".toml"

    # prevent file overwrite?
    if not allow_overwrite and path.exists(filepath):
        print(strings.SKIP.format(strings.SKIP_NO_CLOBBER) + '\n')
        return False

    # ---- writing. ---- #

    makedirs(dirname(filepath), exist_ok=True)

    toml_filepath: str = filepath
    toml_data: TOMLDocument = tomlkit.document()

    for key in data:
        toml_data.add(key, data[key])

    with open(toml_filepath, "w", encoding="utf-8") as toml_record:
        toml_record.write(tomlkit.dumps(toml_data))

    print(f"wrote {toml_filepath}")
    return True
