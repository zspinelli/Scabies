"""
CURRENT KNOWN ISSUES:
- no linux support
- no mac support
- no cookies from safari
- no cookies from chrome
- no cookies from brave
"""

# stdlib.
import binascii, random, re, sqlite3
from argparse import ArgumentParser, Namespace
from http.cookiejar import Cookie
from os import listdir, path, environ
from platform import system

# scraping.
from requests import Session


def _load_cookies_chrome(session: Session):
    pass


def _load_cookies_firefox(session: Session):
    print("loading firefox cookies...")

    PROFILE_HOME_DIR: str = path.join(environ["USERPROFILE"], "Appdata\\Roaming\\Mozilla\\Firefox\\Profiles")

    # ---- find and open cookie database. ---- #

    cookies_db_filepath: str = ""
    db: sqlite3.Connection | None = None

    for found in listdir(PROFILE_HOME_DIR):
        # match found.
        if re.match(r"\w{8}\.default-release", found):
            cookies_db_filepath = path.join(PROFILE_HOME_DIR, found, "cookies.sqlite")
            print("found cookie database:", cookies_db_filepath)

            db = sqlite3.connect(cookies_db_filepath)

            # ---- read records. ---- #

            #sql: str = "SELECT * FROM sqlite_master WHERE type='table';"
            # for found in db.execute(sql).fetchall(): print(found)

            sql: str = "SELECT name, value, host, path, isSecure, expiry FROM moz_cookies"

            for name, value, domain, url_path, secure, expires in db.execute(sql):
                session.cookies.set_cookie(Cookie(
                    0,
                    name,
                    value,
                    None,
                    False,
                    domain,
                    bool(domain),
                    domain.startswith("."),
                    url_path,
                    bool(url_path),
                    secure,
                    expires,
                    False,
                    None,
                    None,
                    {}
                ))

            break


def _load_cookies_safari(session: Session):
    pass


_LINUX: str = "linux"
_MAC: str = "darwin"
_WINDOWS: str = "windows"

_CHROME: str = "chrome"
_FIREFOX: str = "firefox"
_SAFARI: str = "safari"

_BROWSERS: dict = {
    _LINUX: [_CHROME, _FIREFOX],
    _MAC: [_CHROME, _FIREFOX, _SAFARI],
    _WINDOWS: [_CHROME, _FIREFOX]
}

_LOADERS: dict = {
    _CHROME: _load_cookies_chrome,
    _FIREFOX: _load_cookies_firefox,
    _SAFARI: _load_cookies_safari
}


def add_cookie_args(parser: ArgumentParser, required: bool= False):
    parser.add_argument(
        "-b",
        required=required,
        help="name of browser to use cookies from",
        dest="browser"
    )


def validate_cookie_args(parsed: Namespace, session: Session):
    # cookies wanted.
    if hasattr(parsed, "browser"):
        # current os supports current browser.
        if parsed.browser in _BROWSERS[system().lower()]:
            _LOADERS[parsed.browser](session)


def load_ddos_guard_cookies(session: Session, domain: str):
    # todo: add description.
    if session.cookies.get("__ddg2", domain=domain):
        token = random.getrandbits(16 * 8).to_bytes(16, "big")
        token = binascii.hexlify(token).decode()

        session.cookies.set("__ddg2", token, domain=domain)


if __name__ == "__main__":
    """
    run this script to test cookie loading.
    parameters need to be passed in from the command line.
    """

    from requests import session, Session

    sess: Session = session()

    parser: ArgumentParser = ArgumentParser()
    add_cookie_args(parser)

    argv: Namespace = parser.parse_args()

    validate_cookie_args(argv, sess)
