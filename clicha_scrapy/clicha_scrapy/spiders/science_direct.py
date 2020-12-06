import scrapy
import logging
from scrapy.spiders import SitemapSpider
from scrapy.http import TextResponse
from twisted.python.failure import Failure
from scrapy.spidermiddlewares.httperror import HttpError


class ScienceDirectSpider(SitemapSpider):
    """A class used to crawl the ScienceDirect site for scholarly articles."""

    name = 'SD'
    # only search this website for articles
    allowed_domains = ['sciencedirect.com']
    sitemap_urls = ['https://www.sciencedirect.com/sitemap.xml']

    num_of_articles = 0
    # count the number of http errors (e.g. 403)
    http_error_counter = 0


    def closed(self, reason: str):
        logging.info("The number of articles found is " + str(self.num_of_articles))
        logging.info("The nmuber of HttpError is" + str(self.http_error_counter))

    def parse(self, response: TextResponse):
        """Parse the sitemaps to count the number of articles."""
        self.num_of_articles += 1

    def parse_article(self, response: TextResponse):
        title = response.xpath('//span[contains(@class, "title-text")]/text()').get().strip()
        date = response.xpath('//div[@class="Publication"]//div[@class="text-xs"]').getall()
        # potentially a pdf
        if title is None:
            return
        
    def errback(self, failure: Failure):
        if failure.check(HttpError):
            self.http_error_counter += 1