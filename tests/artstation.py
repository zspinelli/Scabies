# scabies.
from scratches.artstation import Artstation


search_url: str = "https://www.artstation.com/search?sort_by=relevance&query=female%20character"
search_args: list = "-os .".split()

user_url: str = ""
user_args: list = "".split()

project_url: str = ""
project_args: list = []

challenge_url: str = ""
challenge_args: list = []

learning_args: list = f"-os . --json-meta --toml-meta user -up Lr ccrumpler".split()


if __name__ == "__main__":
    scraper: Artstation = Artstation()

    scraper.run(search_args)
    scraper.run(user_args)
    scraper.run(project_args)
    scraper.run(challenge_args)
    scraper.run(learning_args)
