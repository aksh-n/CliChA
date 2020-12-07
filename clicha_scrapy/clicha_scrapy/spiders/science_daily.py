import logging
from typing import Dict
import scrapy
from scrapy.http.request import Request

from scrapy.spiders import SitemapSpider
from scrapy.http import TextResponse
from scrapy.utils.sitemap import Sitemap
from scrapy.exceptions import CloseSpider

if __package__ == 'clicha_scrapy.spiders':
    from clicha_scrapy.text_writer import TextWriter


class ScienceDailySpider(SitemapSpider):
    """A class used to crawl the Science Daily site for articles.

    These articles represent the academic side of publication.
    """

    name = 'SDaily'
    allowed_domains = ['sciencedaily.com']
    sitemap_urls = ['https://www.sciencedaily.com/sitemap-index.xml']
    # only follow sitemaps that point to articles
    sitemap_follow = ['sitemap-releases']
    writers: Dict[int, TextWriter] = {}

    def closed(self, reason: str):
        for writer in self.writers.values():
            writer.close()

    
    def parse(self, response: TextResponse):
        """Parse each article to extract its text."""
        date = response.xpath('//dd[@id="date_posted"]/text()').get()

        try:
            year = int(date.split(',')[1])
        except Exception:
            return

        title = response.xpath('//h1[@id="headline"]/text()').get().strip()
        first = str.join(' ', (s.strip() for s in response.xpath(
                         '//div[@id="story_text"]/p/descendant-or-self::*/text()'
                         ).getall()))
        
        txt = str.join(' ', (s.strip() for s in response.xpath(
                       '//div[@id="story_text"]/div[@id="text"]/p/descendant-or-self::*/text()'
                       ).getall()))

        if year not in self.writers:
            self.writers[year] = TextWriter(f'science_daily_text/{year}.txt')

        self.writers[year].append_article(title + '\n' + first + ' ' + txt)
        
        
        # if self.writer.counter >= self.NUM_CAP:
        #     raise CloseSpider('Max article limit reached')


    # def sitemap_filter(self: 'TStarSpider', entries: Sitemap):
    #     count = 0
        
    #     for entry in entries:
    #         if count <= self.NUM_CAP_PER_SITEMAP:
    #             yield entry
    #         count += 1
