"""Climate Change Awareness (CliChA), Science Daily Scraper

This module contains the ScienceDailySpider, a Scrapy spider that crawls
'sciencedaily.com' for articles.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from typing import Dict, List
from scrapy.spiders import SitemapSpider
from scrapy.http import TextResponse

if __package__ == 'clicha_scrapy.spiders':
    # if called from Scrapy command line
    from clicha_scrapy.text_writer import TextWriter
else:
    # import from parent directory
    import os
    import sys
    import inspect
    sys.path.append(os.path.dirname(os.path.dirname(inspect.getfile(inspect.currentframe()))))
    from text_writer import TextWriter


class ScienceDailySpider(SitemapSpider):
    """A class used to crawl the Science Daily site for articles.

    These articles are the portion of the data that represent academia.
    The scraped articles are separated by year and stored in the science_daily folder.

    Instance Attributes:
        - (inherited) name: the name of the spider
        - (inherited) allowed_domains: the domain on which the spider is allowed to crawl data
        - (inherited) sitemap_urls: the url(s) containing the initial sitemap(s), where links to
          articles are discovered
        - (inherited) sitemap_follow: a list of regex expression that set the sitemaps to follow
        - writers: a Dict of TextWriters that handle text formatting and output to file, each
          responsible for one year of data
    """

    name: str = 'SDaily'
    allowed_domains: List[str] = ['sciencedaily.com']
    sitemap_urls: List[str] = ['https://www.sciencedaily.com/sitemap-index.xml']
    # only follow sitemaps that point to articles
    sitemap_follow: List[str] = ['sitemap-releases']
    writers: Dict[int, TextWriter] = {}

    def closed(self, reason: str) -> None:
        """Close the writer when the spider closes.

        This function is called automatically by Scrapy upon closing the spider.
        """
        for writer in self.writers.values():
            writer.close()

    def parse(self, response: TextResponse) -> None:
        """Parse each article to extract its content."""
        date = response.xpath('//dd[@id="date_posted"]/text()').get()
        year = int(date.split(',')[1])

        title = response.xpath('//h1[@id="headline"]/text()').get().strip()
        # first refers to the summary section on a given page
        first_path = '//div[@id="story_text"]/p/descendant-or-self::*/text()'
        txt_path = '//div[@id="story_text"]/div[@id="text"]/p/descendant-or-self::*/text()'
        first = str.join(' ', (s.strip() for s in response.xpath(first_path).getall()))
        txt = str.join(' ', (s.strip() for s in response.xpath(txt_path).getall()))

        if year not in self.writers:
            self.writers[year] = TextWriter(f'science_daily/{year}.txt')

        self.writers[year].append_article(title + '\n' + first + ' ' + txt)


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
