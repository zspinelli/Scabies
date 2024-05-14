
class _Codes:
    pass


class SwitchPlate:
    def __init__(self, tokens: dict, default: str=""):
        self.CODES: _Codes = _Codes()
        self._default = default

        for token, code in tokens.items():
            setattr(self, token.upper(), token)
            setattr(self.CODES, token.upper(), code)


    def default(self) -> str:
        return self._default


    def legend(self) -> str:
        legend: list = []

        for name, abrv in vars(self.CODES).items():
            if name != "str" and not callable(abrv) and not name.startswith("__"):
                legend.append(f"{name}: {abrv}")

        legend_concat: str = ", ".join(legend)
        return legend_concat
