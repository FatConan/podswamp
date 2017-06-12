#SPY DB

##Project
Stop Podcasting Yourself Database (SPY DB): extracts guest information and builds a site from the public Libsyn RSS of Stop Podcasting Yourself podcast episodes.

The python scrapes the feed (via __scaper.py__) into the _base.json_ file, then processes that file into a pair of extrapolated files that record guest appearances and statistics (via __process.py__).  Once that data has been established a static HTML site can be generated from the templates (in the __resources/__ folder) using the __html_creation.py__ script.

##Build the HTML
1. Run ```python scraper.py``` to scrape the RSS feed.
2. Run ```python process.py``` to extract the guest information.
3. Run ```python html_creator.py``` to generate the final database site from the previous data.

Once the first two steps have been run you can rerun the third step to repeatedly generate the HML.  This is useful when playing with templates.



