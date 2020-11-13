import logging
import scrapy
from scrapy.http.request import Request

from scrapy.spiders import SitemapSpider
from scrapy.http import TextResponse
from scrapy.utils.sitemap import Sitemap
from scrapy.exceptions import CloseSpider


class TStarSpider(SitemapSpider):
    """A class used to crawl the Toronto Star site for articles.

    These articles are used in conjunction with the NASA articles to process
    and extract climate-change related keywords, to be used in further processing.
    """

    name = 'TStar'
    allowed_domains = ['www.thestar.com']
    # discovers sitemaps through robots.txt
    sitemap_urls = ['https://www.thestar.com/robots.txt']

    sitemap_rules = [('/web-sitemap/', '_parse_sitemap'), ('', 'parse')]

    num_of_articles = 0
    # the max number of articles to crawl
    NUM_CAP = 15000
    NUM_CAP_PER_SITEMAP = 300
    

    def closed(self: "TStarSpider", reason: str):
        with open('tstar.txt', 'a', encoding='utf-8') as f:
            f.write('Articles crawled: ' + str(self.num_of_articles) + '\n')

    
    def parse(self: 'TStarSpider', response: TextResponse):
        """Parse each article to extract its text."""
        title = response.xpath('//h1[contains(@class, "headline")]/text()').get().strip()
        txtlist = response.xpath(
            '//p[contains(@class, "text-block-container")]/text()'
        ).getall()

        txt = str.join(' ', [s.strip() for s in txtlist])

        with open('tstar.txt', 'a', encoding='utf-8') as f:
            f.write(str(self.num_of_articles) + '-> ' + title + '\n' + txt)
            f.write('\n--------\n')
        
        self.num_of_articles += 1
        
        if self.num_of_articles >= self.NUM_CAP:
            raise CloseSpider('Max article limit reached')


    def sitemap_filter(self: 'TStarSpider', entries: Sitemap):
        count = 0
        
        for entry in entries:
            if count <= self.NUM_CAP_PER_SITEMAP:
                yield entry
            count += 1
        