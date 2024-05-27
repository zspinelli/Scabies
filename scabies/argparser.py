
class ArgParser:
    class _Flag:
        def __init__(self, token: chr, dest: str = "", usage: str = ""):
            self._token: chr = token
            self._dest: str = dest
            self._usage: str = usage


    class _Switch:
        def __init__(self):
            self._name: str
            self._dest: str


    def __init__(self, name: str = "", dest: str = "", usage: str = ""):
        self._name: str = name
        self._dest: str = dest
        self._usage: str = usage

        self._flags: list = []
        self._options: list = []
        self._switches: list = []
        self._branches: list = []
        self._remainder: list = []


    def name(self) -> str:  return self._name
    def dest(self) -> str:  return self._dest

    def usage(self) -> str: return self._usage


    def add_flag(self, token: chr, dest: str, usage: str):
        pass


    def add_option(self, token: str, dest: str, usage: str):
        pass


    def add_switch(self, usage: str):
        pass


    def add_branch(self, name: str, dest: str = "", usage: str = ""):
        branch: ArgParser = ArgParser(name, dest if dest else name, usage)
        self._branches.append(branch)

        return branch


    def add_remainder(self, usage: str):
        pass


    def print_usage(self):
        pass


    def parse(self, args: list) -> dict:
        parsed: dict = {}

        while args:
            arg: str = args.pop(0)

            # flag or option.
            if arg.startswith("-"):
                # flags required.
                if self._flags:
                    for flag in self._flags:
                        # match.
                        if arg[1] == flag.token:
                            pass

                # options required.
                if self._options:
                    for opt in self._options:
                        # match.
                        if arg[2:] == opt.token:
                            pass

            # switch.
            elif arg.startswith("--"):
                pass





            if self._flags or self._options:


            # flags required.
            if self._flags:
                # flag.



            # switches required.
            if self._switches:

                if arg.startswith("--"):
                    for switch in self._switches:
                        pass

            # branches required.
            if self._branches:
                for branch in self._branches:
                    pass

            # remainder required.
            if self._remainder:
                pass

        return parsed
