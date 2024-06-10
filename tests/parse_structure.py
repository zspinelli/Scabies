from argparse import ArgumentParser
from sys import argv

# ---- parse args. ---- #

parser = ArgumentParser()
modes = parser.add_subparsers()

modes.add_parser("search")

modes.add_parser("user")

modes.add_parser("post")

args = parser.parse_args(argv[1:])
print("parsed:", args)

# ---- analyze parser. ---- #

for action in parser._actions:
    print(action)
