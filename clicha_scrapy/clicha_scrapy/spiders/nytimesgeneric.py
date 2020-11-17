import logging

import scrapy
from clicha_scrapy.items import ArticleItem
from scrapy.http import Response, TextResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NyTimesSpider(CrawlSpider):
    """A class used to clawl the NYTimes website for articles.

    This crawler crawls ALL the available articles listed on the NYTimes
    sitemap. It then extracts their titles and saves them in a separate file
    for each year.

    Call this crawler by using typing "scrapy crawl nytimes -a start=START -a end=END", where
    START and END should be replaced by the desired starting and ending years.
    """
    name = 'nytimes'
    allowed_domains = ['nytimes.com']

    start_url = 'https://spiderbites.nytimes.com'

    def start_requests(self):
        # supply command-line arguments with -a
        start_year = int(getattr(self, 'start'))
        end_year = int(getattr(self, 'end'))

        for i in range(start_year, end_year + 1):
            url = self.start_url + '/' + str(i) + '/'
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'year': i})


    def parse(self, response: TextResponse, year: int):
        for a in response.xpath('//div[contains(@class, "articlesMonth")]/ul/li/a'):
            yield response.follow(a, callback=self.parse_articles, cb_kwargs={'year': year})


    def parse_articles(self, response: TextResponse, year: int):
        """Parse each month-part page extracted by parse."""
        for a in response.xpath('//ul[@id="headlines"]/li/a'):
            yield response.follow(a, callback=self.parse_article, cb_kwargs={'year': year})


    def parse_article(self, response: TextResponse, year: int):
        item = ArticleItem()

        item['headline'] = response.xpath(
            '//h1[@itemprop="headline"]/text()').get()

        with open(f'./nytimes/{year}.txt', 'a', encoding='utf-8') as f:
            f.write(item['headline'].strip())
            f.write('\n')
