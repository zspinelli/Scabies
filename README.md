
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

SCRAPER MODES

most scrapers have a mode called "user", this is the one that will typically allow collection of your own favorite posts and creators by targeting it at your own account. 

some scrapers have a mode called "scrape" these are for brute force collection of "all accounts on the site" or similar. it's for helping gigantic site-wide archives or metadata collection
to implement alternative search engines.

OTHER

if you decide to try scabies, don't hesitate to submit an issue if you find it behaving incorrectly, as a single developer with multiple
other projects and hobbies, it's easy for me to forget to fully test for bugs. it is in my plans to make tests for each feature eventually
once the overall structure of the scraper collection stops changing so drastically and all the capabilites and characteristics i want are visible
in the design.

don't hestitate to ask about helping either, if there is a site you want covered that i'm not currently making or a feature you want
from scrapers i already made.
