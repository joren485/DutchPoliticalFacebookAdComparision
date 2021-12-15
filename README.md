# DutchPoliticalFacebookAdComparision

This repo contains all data and code used to publish https://joren485.github.io/DutchPoliticalFacebookAdComparision/, a website that compares and aggregates statistics about Facebook advertisements by Dutch political parties. It is based on data from [the Facebook Ad Library](https://www.facebook.com/ads/library/). It consists of three parts: the data, the code and the website files. For more info on the data that you see on the website, please visit the [about page](https://joren485.github.io/DutchPoliticalFacebookAdComparision/website/about.html).

### The Data
The [`data`](data/) directory contains [a list of Facebook pages that are used by Dutch political parties](data/facebook_page_ids.csv). It also contains wordlists used in the theme analysis.

### The Code
The [`parsing`](parsing/) directory contains the code that downloads, parses and analyses the data. The [`templates`](templates/) directory contains Jinja2 template HTML files that are used by the code to render the final website.

- [`download.py`](parsing/download.py): Takes the list of Facebook pages in the data directory and downloads Facebook ads ran by those pages. It saves all found ads in a SQLite database (in [`data`](data/)).
  - This requires a Facebook token to run. Please see the [Facebook Ad Library API documentation](https://www.facebook.com/ads/library/api/) for further information.
- [`processing-general.py`](parsing/processing-general.py): Analyses the ads in the database to render the index and about pages.
- [`processing-party.py`](parsing/processing-party.py): Analyses the ads in the database to render the party specific pages.
- [`processing-themes.py`](parsing/processing-themes.py): Analyses the ads in the database to render the themes page.
- [`parse_pages.py`](parsing/parse_pages.py): A small standalone script that creates a list of Facebook pages used by Dutch political parties in the data directory. Please note that the output of this script contains many false positives.
- [`charts.js`](website/js/charts.js) contains Javascript code to render the graphs.


### The Website
[index.html](index.html) and the [website](website/) directory contain the rendered website. [GitHub Pages](https://pages.github.com/) serves these.
