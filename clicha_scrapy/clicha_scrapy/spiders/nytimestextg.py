import os
import logging
import scrapy
from scrapy.exceptions import CloseSpider
from clicha_scrapy.items import ArticleItem
from scrapy.http import Response, TextResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class NyTimesTextSpider(CrawlSpider):
    """A class used to clawl the NYTimes website for articles.

    This crawler is different from the other NYTimes spider in that it only crawls a limited
    number of articles from each year. However, in addition to their titles, it also stores their
    bodies (text).
    """

    name = 'nytimestext'
    allowed_domains = ['nytimes.com']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'clicha_scrapy.middlewares.ClichaScrapyDownloaderMiddleware': 000}
    }

    start_url = 'https://spiderbites.nytimes.com'

    # keeps track of the number of articles already crawled for each year
    num_counter = {}
    # the number of articles to crawl from each year
    NUM_PER_YEAR = 500

    def start_requests(self):
        # supply command-line arguments with -a
        start_year = int(getattr(self, 'start'))
        end_year = int(getattr(self, 'end'))

        for i in range(start_year, end_year + 1):
            self.num_counter[i] = 0
            url = self.start_url + '/' + str(i) + '/'
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'year': i})


    def parse(self, response: TextResponse, year: int):
        """Parse the root page of each year as requested by start_requests."""
        if self.num_counter[year] >= self.NUM_PER_YEAR:
            return
                   
        for a in response.xpath('//div[contains(@class, "articlesMonth")]/ul/li/a'):
            yield response.follow(a, callback=self.parse_articles, cb_kwargs={'year': year})


    def parse_articles(self, response: TextResponse, year: int):
        """Parse each month-part page extracted by parse."""
        if self.num_counter[year] >= self.NUM_PER_YEAR:
            return

        for a in response.xpath('//ul[@id="headlines"]/li/a'):
            # the meta component is used by the middleware te decide
            # whether or not to drop the request based on articles already processed
            yield response.follow(a, callback=self.parse_article, meta={'year': year}, cb_kwargs={'year': year})


    def parse_article(self: "NyTimesTextSpider", response: TextResponse, year: int):
        if self.num_counter[year] >= self.NUM_PER_YEAR:
            return

        headline = response.xpath('//h1[@itemprop="headline"]/text()').get().strip()
        txtlist = response.xpath('//section[contains(@name, "articleBody")]//p/text()').getall()
        time = response.xpath('//header//time/text()').get()
        txt = str.join(' ', [s.strip() for s in txtlist])

        with open(f'./nytimestext/{year}.txt', 'a') as f:
            # TODO delete the timestamp
            f.write(time + '-> ' + str(self.num_counter[year]) + '-> ' + headline + '\n' + txt)
            f.write('\n--------\n')

        self.num_counter[year] += 1
        if self.num_counter[year] >= self.NUM_PER_YEAR and all({x >= self.NUM_PER_YEAR for x in self.num_counter.values()}):
            raise CloseSpider("Job finished")
