"""Climate Change Awareness, NYTimes Scraper

This module contains the NyTimesTextSpider, a Scrapy spider that crawls
'nytimes.com' for articles.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from typing import Any, Dict, Iterator, List, Optional
from random import randint
from scrapy.exceptions import CloseSpider
from scrapy.http import TextResponse, Request
from scrapy.spiders import CrawlSpider

if __package__ == 'clicha_scrapy.spiders':
    from clicha_scrapy.text_writer import TextWriter
else:
    # import from parent directory
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from text_writer import TextWriter


class NyTimesTextSpider(CrawlSpider):
    """A class used to clawl the NYTimes website for articles.

    These articles are the portion of the data that represent mainstream media.
    The scraped articles are separated by year and stored in the 'nytimes' folder.

    Instance Attributes:
        - (inherited) name: the name of the spider
        - (inherited) allowed_domains: the domain on which the spider is allowed to crawl data
        - (inherited) custom_settings: settings that are overridden; in this case, an extra
          middleware is added to speed up data extraction; see middlewares.py for details
        - base_url: the base url of NYTimes sitemaps
        - writers: a Dict of TextWriters that handle text formatting and output to file, each
          responsible for one year of data
        - NUM_PER_YEAR: the maximum number of articles to scrapy for each year
    """

    name: str = 'nytimestext'
    allowed_domains: List[str] = ['spiderbites.nytimes.com', 'www.nytimes.com']
    custom_settings: Dict[str, Any] = {
        'DOWNLOADER_MIDDLEWARES': {
            'clicha_scrapy.middlewares.ClichaScrapyDownloaderMiddleware': 000
        }
    }
    base_url: str = 'https://spiderbites.nytimes.com'
    writers: Dict[int, TextWriter] = {}
    NUM_PER_YEAR: int = 1500

    def closed(self, reason: str) -> None:
        """Close the writer when the spider closes.

        This function is called automatically by Scrapy upon closing the spider.
        """
        for writer in self.writers.values():
            writer.close()

    def start_requests(self) -> Iterator[Request]:
        """Initiate the scraping process by yielding requests to each year's sitemap page.

        This function is called automatically by Scrapy when scraping starts.
        """
        # the start end end years can be configured from the command line
        start_year = int(getattr(self, 'start'))
        end_year = int(getattr(self, 'end'))

        for i in range(start_year, end_year + 1):
            url = self.base_url + '/' + str(i) + '/'
            yield Request(url=url, callback=self.parse, cb_kwargs={'year': i})

    def parse(self, response: TextResponse, year: int) -> Iterator[Request]:
        """Parse the responses as requested by start_requests to extract sub-level links."""
        if year in self.writers and self.writers[year].counter >= self.NUM_PER_YEAR:
            return

        # set priority to 10 to always process these first
        for each in response.xpath('//div[contains(@class, "articlesMonth")]/ul/li/a'):
            yield response.follow(
                each,
                priority=10,
                callback=self.parse_sub,
                cb_kwargs={'year': year}
            )

    def parse_sub(self, response: TextResponse, year: int) -> Iterator[Request]:
        """Parse the responses as requested by parse to extract article links."""
        if year in self.writers and self.writers[year].counter >= self.NUM_PER_YEAR:
            return

        for each in response.xpath('//ul[@id="headlines"]/li/a'):
            # the meta component is used by the middleware te decide
            # whether or not to drop the request based on articles already processed
            yield response.follow(
                each,
                callback=self.parse_article,
                priority=randint(0, 9),
                meta={'year': year},
                cb_kwargs={'year': year}
            )

    def parse_article(
            self: "NyTimesTextSpider",
            response: TextResponse, year: int
    ) -> Optional[Iterator[Request]]:
        """Parse each article to extract its content."""
        if year in self.writers and self.writers[year].counter >= self.NUM_PER_YEAR:
            return

        headline = response.xpath('//h1[@itemprop="headline"]/text()').get()
        # exclude CN nytimes pages
        if headline is None:
            return
        headline = headline.strip()

        txtlist = response.xpath('//section[contains(@name, "articleBody")]//p/text()').getall()
        txt = str.join(' ', (s.strip() for s in txtlist))
        # exclude articles whose bodies are empty
        if not txt or txt.isspace():
            return

        if year not in self.writers:
            self.writers[year] = TextWriter(f'./nytimes/{year}.txt')
        self.writers[year].append_article(headline + '\n' + txt)

        # early exit if there are enough articles already
        if self.writers[year].counter >= self.NUM_PER_YEAR\
            and all(writer.counter >= self.NUM_PER_YEAR
                    for writer in self.writers.values()):
            raise CloseSpider("Job finished")


if __name__ == '__main__':
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
