# scabies.
from scabies.scraper import MetaScraper


class FelthierMeta(MetaScraper):
    def __init__(self):
        super().__init__(
            "felthier-meta-all-usernames",
            "g6jy5jkx466lrqojcngbnksugrcfxsl562bzuikrka5rv7srgguqbjid.onion/fa",
            self._thread_task,
            self._print_stats
        )


    def _parse_args(self, args: list):
        pass


    def run(self, args: list):
        pass


    def _thread_task(self):
        pass


    def _print_stats(self):
        pass


def run(args: list):
    scraper: FelthierMeta = FelthierMeta()
    scraper.run(args)


if __name__ == "__main__":
    from sys import argv, exit

    run(argv)
    exit(0)
