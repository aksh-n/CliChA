import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Response

# this spider now finds every link on the cbc home page
class CbctestSpider(CrawlSpider):
    name = 'cbctest'
    allowed_domains = ['www.cbc.ca']
    start_urls = ['http://www.cbc.ca/']
    rules = (
        Rule(LinkExtractor(allow='^http://www.cbc.ca/$'), callback='parse', follow=True),
        Rule(LinkExtractor(), callback='parse', follow=False)
    )

    def parse(self, response: Response):
        yield {'url': response.url}