# stdlib.
from datetime import datetime
from os import name
from time import sleep

# scraping.
from requests import Session, Response
from requests.adapters import HTTPAdapter


_HTTP_HEADERS: tuple = (
    ("User-Agent", "Mozilla/5.0 ({}; rv:102.0) Gecko/20100101 Firefox/102.0"),
    ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"),
    ("Accept-Language", "en-US,en;q=0.5"),
    ("Accept-Encoding", "gzip, deflate"),
    ("Referer", None),
    ("DNT", "1"),
    ("Connection", "keep-alive"),
    ("Upgrade-Insecure-Requests", "1"),
    ("Cookie", None),
    ("Sec-Fetch-Dest", "empty"),
    ("Sec-Fetch-Mode", "no-cors"),
    ("Sec-Fetch-Site", "same-origin"),
    ("TE", "trailers")
)


class ScabiesSession(Session):
    def __init__(self, interval: int = 0):
        super().__init__()

        self._request_interval: int = interval
        self._last_request_timestamp: datetime = datetime.max

        self.headers.clear()

        platform: str = ""

        # choose header system name by platform.
        if name == "nt":    platform = "Windows NT 10.0; Win64; x64"
        else:               platform = "X11; Linux x86_64"

        for k, v in _HTTP_HEADERS:
            if v and "{}" in v:     self.headers[k] = v.format(platform)
            else:                   self.headers[k] = v

        adapter: HTTPAdapter = HTTPAdapter()

        self.mount("https://", adapter)
        self.mount("http://", adapter)


    def _enforce_interval(self):
        # no previous request.
        if self._last_request_timestamp > datetime.now():
            self._last_request_timestamp = datetime.now()
            return

        # previous request made.
        else:
            time_elapsed: float = (datetime.now() - self._last_request_timestamp).total_seconds()
            print("time_elapsed:", time_elapsed)

            # required time interval not elapsed.
            if time_elapsed < self._request_interval:
                time_to_sleep: float = self._request_interval - time_elapsed
                print(f"required interval ({self._request_interval}) has not elapsed. waiting:", time_to_sleep, "seconds...")
                sleep(time_to_sleep)


    def get(self, url, **kwargs) -> Response:
        # enforce request interval.
        if self._request_interval != 0:
            self._enforce_interval()

        response: Response = super().get(url, **kwargs)
        self._last_request_timestamp = datetime.now()

        return response


    def post(self, url, **kwargs) -> Response:
        # enforce request interval.
        if self._request_interval > 0:
            self._enforce_interval()

        response: Response = super().post(url, **kwargs)
        self._last_request_time = datetime.now()

        return response


    def request(self, method, url, **kwargs) -> Response:
        # enforce request interval.
        if self._request_interval > 0:
            self._enforce_interval()

        response: Response = super().request(method, url, **kwargs)
        self._last_request_time = datetime.now()

        return response


def new(interval: int) -> ScabiesSession:
    sess: ScabiesSession = ScabiesSession(interval)
    return sess
