"""Climate Change Awareness (ChiChA), NASA Scraper

This module contains the NASASpider, a Scrapy spider that crawls 'climate.nasa.gov' for
climate change related articles.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from typing import List
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


class NASASpider(SitemapSpider):
    """A class that crawls the NASA climate change site for climate change related articles.

    Keywords are extracted from these articles to then be used on other articles to calculate
    the Climate Change Awareness Index. The scraped articles are stored in 'nasa.txt'.

    Instance Attributes:
        - (inherited) name: the name of the spider
        - (inherited) allowed_domains: the domain on which the spider is allowed to crawl data
        - (inherited) sitemap_urls: the url(s) containing the initial sitemap(s), where links to
          articles are discovered
        - writer: a TextWriter that handles text formatting and output to file
    """

    name: str = 'NASA'
    allowed_domains: List[str] = ['climate.nasa.gov']
    sitemap_urls: List[str] = ['https://climate.nasa.gov/sitemaps/news_items_sitemap.xml']
    writer: TextWriter

    def closed(self, reason: str) -> None:
        """Close the writer when the spider closes.

        This function is called automatically by Scrapy upon closing the spider.
        """
        self.writer.close()

    def parse(self, response: TextResponse) -> None:
        """Parse each article to extract its content.

        This function is called automatically by Scrapy for every link discovered.
        """
        title = response.xpath('//h1[contains(@class, "article_title")]/text()').get().strip()
        txtlist = response.xpath(
            '(//div[contains(@class, "wysiwyg_content")]//p'
            '| //div[contains(@class, "wysiwyg_content")]//h3)'
            '/descendant-or-self::*/text()'
        ).getall()

        txt = str.join(' ', [s.strip() for s in txtlist])

        self.writer.append_article(title + '\n' + txt)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['*'],
        'extra-imports': ['scrapy',
                          'scrapy.spiders',
                          'scrapy.http',
                          'text_writer',
                          'clicha_scrapy.text_writer',
                          'os',
                          'sys',
                          'inspect',
                          'doctest',
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
