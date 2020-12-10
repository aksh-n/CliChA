"""Climate Change Awareness (CliChA), TStar Scraper

This module contains the TStarSpider, a Scrapy spider that crawls
'thestar.com' for articles.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from typing import List, Tuple, Iterator
from scrapy.spiders import SitemapSpider
from scrapy.http import TextResponse
from scrapy.utils.sitemap import Sitemap
from scrapy.exceptions import CloseSpider

if __package__ == 'clicha_scrapy.spiders':
    from clicha_scrapy.text_writer import TextWriter
else:
    # import from parent directory
    import os
    import sys
    import inspect
    sys.path.append(os.path.dirname(os.path.dirname(inspect.getfile(inspect.currentframe()))))
    from text_writer import TextWriter


class TStarSpider(SitemapSpider):
    """A class used to crawl the Toronto Star site for articles.

    These articles are used in conjunction with the NASA and UN articles to process
    and extract climate-change related keywords, which are then used in further processing.
    Note that these articles themselves are not climate change articles necessarily, but are
    included to offset some common words that are not climate change related but are found
    in climate change articles nonetheless. The scraped articles are stored in 'tstar.txt'.

    Instance Attributes:
        - (inherited) name: the name of the spider
        - (inherited) allowed_domains: the domain on which the spider is allowed to crawl data
        - (inherited) sitemap_urls: the url(s) containing the initial sitemap(s), where links to
          articles are discovered
        - (inherited) sitemap_rules: a lits of rules assigning each extracted link to be
          processed by a specific parse method
        - writer: a TextWriter that handles text formatting and output to file
        - NUM_CAP: the max number of articles to crawl
        - NUM_CAP_PER_SITEMAP: the max number of articles to crawl per sitemap
    """

    name: str = 'TStar'
    allowed_domains: List[str] = ['www.thestar.com']
    # discovers sitemaps through robots.txt
    sitemap_urls: List[str] = ['https://www.thestar.com/robots.txt']
    sitemap_rules: List[Tuple[str, str]] = [('/web-sitemap/', '_parse_sitemap'), ('', 'parse')]
    writer: TextWriter = TextWriter('tstar.txt')
    # the max number of articles to crawl
    NUM_CAP: int = 15000
    NUM_CAP_PER_SITEMAP: int = 300

    def closed(self, reason: str) -> None:
        """Close the writer when the spider closes.

        This function is called automatically by Scrapy upon closing the spider.
        """
        self.writer.close()

    def parse(self, response: TextResponse) -> None:
        """Parse each article to extract its content."""
        title = response.xpath('//h1[contains(@class, "headline")]/text()').get().strip()
        txt_path = '//p[contains(@class, "text-block-container")]/text()'
        txtlist = response.xpath(txt_path).getall()
        txt = str.join(' ', [s.strip() for s in txtlist])

        self.writer.append_article(title + '\n' + txt)

        if self.writer.counter >= self.NUM_CAP:
            raise CloseSpider('Max article limit reached')

    def sitemap_filter(self, entries: Sitemap) -> Iterator:
        """Limit the number of articles each sitemap can provide to improve randomness."""
        count = 0

        for entry in entries:
            if count <= self.NUM_CAP_PER_SITEMAP:
                yield entry
            else:
                return
            count += 1


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['*'],
        'extra-imports': ['scrapy',
                          'scrapy.spiders',
                          'scrapy.http',
                          'scrapy.exceptions',
                          'scrapy.utils.sitemap',
                          'text_writer',
                          'clicha_scrapy.text_writer',
                          'random',
                          'typing',
                          'os',
                          'sys',
                          'inspect',
                          'python_ta.contracts'],
        'max-line-length': 100,
        'max-args': 6,
        'max-locals': 25,
        # W0221: by the documentation, parse does not need **kwargs
        # W0613: 'closed' is called by Scrapy, requiring the 'reason' argument
        'disable': ['R1705', 'W0221', 'W0613'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
