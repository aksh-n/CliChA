"""Climate Change Awareness (CliChA), UN Scraper

This module contains the UNSpider, a Scrapy spider that crawls
'news.un.org' for climate change related articles.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from typing import Iterator, List
from scrapy.spiders import Spider
from scrapy.http import TextResponse, Request

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


class UNSpider(Spider):
    """A class used to crawl the UN climate change site for climate change related articles.

    These articles are used in conjunction with the NASA and TStar articles to process
    and extract climate-change related keywords, which are then used in further processing.
    The scraped articles are stored in 'un.txt'.

    Instance Attributes:
        - (inherited) name: the name of the spider
        - (inherited) allowed_domains: the domain on which the spider is allowed to crawl data
        - writer: a TextWriter that handles text formatting and output to file
    """

    name: str = 'UN'
    allowed_domains: List[str] = ['news.un.org']
    writer: TextWriter = TextWriter('un.txt')

    def closed(self, reason: str) -> None:
        """Close the writer when the spider closes.

        This function is called automatically by Scrapy upon closing the spider.
        """
        self.writer.close()

    def start_requests(self) -> Iterator[Request]:
        """Initiate the scraping process by yielding requests to each page containing
        links to articles to be crawled.

        This function is called automatically by Scrapy when scraping starts.
        """
        base_url = 'https://news.un.org/en/news/topic/climate-change'

        # 51 pages in total
        for page_num in range(1, 52):
            yield Request(base_url + '?page=' + str(page_num), callback=self.parse)

    def parse(self, response: TextResponse) -> Iterator[Request]:
        """Parse each catalog page and extract article links."""
        for each in response.xpath('//div[@class="view-content"]//h1/a/@href').getall():
            yield response.follow(each, callback=self.parse_article)

    def parse_article(self, response: TextResponse) -> None:
        """Parse each article to extract its content."""
        title = response.xpath('//h1/text()').get().strip()
        body_path = '(//div[@class="content"]//p | //div[@class="content"]//h3)/text()'
        body = str.join(' ', (each.strip() for each in response.xpath(body_path).getall()))
        # avoid empty-bodied articles
        if not body or body.isspace():
            return

        self.writer.append_article(title + '\n' + body)


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
