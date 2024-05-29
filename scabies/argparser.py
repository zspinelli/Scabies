# stdlib.
from copy import deepcopy


class _Arg:
    def __init__(self):
        self._token: str = ""
        self._name: str = ""
        self._usage: str = ""


    def token(self) -> str: return self._token
    def dest(self) -> str:  return self._name
    def usage(self) -> str: return self._usage


class _Switch(_Arg):
    def __init__(
        self,
        token: str,
        dest: str,
        usage: str = ""
    ):
        super().__init__(token)

        self._dest = dest
        self._usage = usage


class _Option(_Switch):
    def __init__(
        self,
        token: str,
        dest: str = "",
        usage: str = "",
        validator = None
    ):
        super().__init__(token, dest, usage)


        self._validator = validator


class _Remainder:
    def __init__(self):
        self._values: list = []


    def append(self, value: str):
        self._values.append(value)


class ArgParser:
    def __init__(
        self,
        name: str = "",
        dest: str = "",
        usage: str = ""
    ):
        self._name: str = name
        self._dest: str = dest
        self._usage: str = usage

        self._switches: list = []
        self._options: list = []
        self._branches: list = []
        self._remainder: _Remainder | None = None


    def name(self) -> str:  return self._name
    def dest(self) -> str:  return self._dest

    def usage(self) -> str: return self._usage


    def add_option(
        self,
        token: str,
        dest: str = "",
        usage: str = ""
    ):
        pass


    def add_switch(
        self,
        token: str,
        off_value: bool,
        usage: str = ""
    ):
        pass


    def add_branch(self, name: str, dest: str = "", usage: str = ""):
        branch: ArgParser = ArgParser(name, dest if dest else name, usage)
        self._branches.append(branch)

        return branch


    def add_remainder(self, dest: str, usage: str = ""):
        pass


    def print_usage(self):
        use_msg: str = ""

        print(use_msg)


    def structure(self):
        structure: dict = {}

        for switch in self._switches:
            structure.update({switch.token(): {

            }})

        for option in self._options:
            structure.update({option.token(): {

            }})

        for branch in self._branches:
            structure.update({branch.name: branch.structure()})

        return structure

    structure.__doc__ = "returns a dict of all the configurable parameters that will be parsed"


    def parse(self, args: list[str]) -> dict:
        args_copy: list = deepcopy(args)
        parsed: dict = {}

        while args:
            arg: str = args.pop(0)

            # ---- responders. ---- #

            # version print.
            if arg in ["/v", "/version"]:
                return {}

            # help print.
            elif arg in ["/h", "/help"]:
                self.print_usage()
                return {}

            # ---- parameters. ---- #

            # long switch.
            if arg.startswith("--") and self._switches:
                for switch in self._switches:
                    # match.
                    if arg[2:] == switch.token():
                        pass

            # short switch.
            elif arg.startswith("-") and self._switches:
                for switch in self._switches:
                    # match.
                    if arg[1:] == switch.token():
                        pass

            # option.
            elif arg.endswith("=") and self._options:
                for opt in self._options:
                        # match.
                        if arg[2:] == opt.token:
                            pass

            # branches required.
            elif self._branches:
                for branch in self._branches:
                    # match.
                    if arg == branch.name():
                        pass

            # remainder required.
            elif self._remainder:
                self._remainder.append(arg)

            # unhandled.
            else:
                pass

        return parsed
