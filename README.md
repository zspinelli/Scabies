
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

OTHER

If you decide to try Scabies, don't hesitate to submit an issue if you find it behaving incorrectly, as a single developer with multiple
other projects and hobbies, it's easy for me to forget to fully test for bugs. It is in my plans to make tests for each feature eventually
once the overall structure of the scraper collection stops changing so drastically and all the capabilites and characteristics I want are visible
in the design.

Don't hestitate to ask about helping either, if there is a site you want covered that I'm not currently making or a feature you want
from scrapers I already made.
