
OVERVIEW

The Scabies project includes the following important structural landmarks:

- cli.py
- docs/
- helpers/
- scabies/
- tests/

cli.py is an entrypoint for terminal and command line interaction.
it contains a curses-based ui to easily and quickly alter the config.

docs/ is designed to hold basic text format documentation, most of that will be created in the future.

helpers/ contains utility programs that may provide useful capabilities to pair with the main scraping goals.
such as polling for usernames.

scabies/ contains shared functionality used by the scrapers.

scratches/ contains the main scraper scripts. each script is written in a way that can be used standalone.