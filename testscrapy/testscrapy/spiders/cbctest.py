"""This is just a test file. Not intended to be used in project."""
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Response


class CbctestSpider(CrawlSpider):
    """This test class finds links on the CBC homepage."""
    name = 'cbctest'
    allowed_domains = ['www.cbc.ca']
    start_urls = ['http://www.cbc.ca/']
    rules = (
        Rule(LinkExtractor(allow='^http://www.cbc.ca/$'),
             callback='parse', follow=True),
        Rule(LinkExtractor(), callback='parse', follow=False)
    )

    def parse(self, response: Response):
        yield {'url': response.url}
