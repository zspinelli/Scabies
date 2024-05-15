# scabies.
from scratches.neo_felthier import Felthier


user_name: str = "commissionsbyj"
user_args: list = f"-os . user --json-meta --toml-meta f{user_name}".split()


if __name__ == "__main__":
    scraper: Felthier = Felthier()
    scraper.run(user_args)
