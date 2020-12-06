import logging
import re
import scrapy
from scrapy.http.request import Request

from scrapy.spiders import SitemapSpider, Spider
from scrapy.http import TextResponse
from scrapy.spiders.crawl import CrawlSpider
from scrapy.utils.sitemap import Sitemap
from scrapy.exceptions import CloseSpider


class JSTORSpider(Spider):
    """A class used to crawl the JSTOR site for articles.

    These articles represent the academic articles portion of the project.
    """

    name = 'JSTOR'
    allowed_domains = ['www.jstor.org']
    # discovers sitemaps through robots.txt
    # sitemap_urls = ['http://www.jstor.org/sitemap.xml']

    start_urls = ['https://www.jstor.org/stable/42934206?seq=1#metadata_info_tab_contents']

    expr = re.compile(r'(/stable/)(\d+)(.*)')

    # num_of_articles = 0
    # # the max number of articles to crawl
    # NUM_CAP = 15000
    # NUM_CAP_PER_SITEMAP = 300

    # def closed(self: "JSTORSpider", reason: str):
    #     with open('tstar.txt', 'a', encoding='utf-8') as f:
    #         f.write('Articles crawled: ' + str(self.num_of_articles) + '\n')


    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.actual_parse)

    
    def parse(self: 'JSTORSpider', response: TextResponse):
        """Parse test."""
        logging.info(response.xpath('//div[contains(@class, "download-button")]/a/@href').get())
        with open('see.html', 'wb') as f:
            f.write(response.body)

    def actual_parse(self: 'JSTORSpider', response: TextResponse):
        new_url = self.expr.sub(r'\1pdf/\2.pdf?refreqid=excelsior%3A038a799c3e34bde64e26bec6b80b852e', str(response.url))
        yield Request(new_url, callback=self.parse_next)


    def parse_next(self: 'JSTORSpider', response: TextResponse):
        logging.info(response.url)

    # def sitemap_filter(self: 'JSTORSpider', entries: Sitemap):
    #     count = 0
        
    #     for entry in entries:
    #         if count <= self.NUM_CAP_PER_SITEMAP:
    #             yield entry
    #         count += 1
