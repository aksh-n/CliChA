import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.http import TextResponse


class TStarSpider(SitemapSpider):
    """A class used to crawl the Toronto Star site for articles.

    These articles are used in conjunction with the NASA articles to process
    and extract climate-change related keywords, to be used in further processing.
    """

    name = 'TStar'
    allowed_domains = ['www.thestar.com']
    # this sitemap contains recent articles on Toronto Star
    sitemap_urls = ['https://www.thestar.com/news-sitemap.xml']

    def parse(self: 'TStarSpider', response: TextResponse):
        """Parse each article to extract its text."""
        txt = str.join('', response.xpath(
            '//p[@class="text-block-container"]/text()').getall())

        with open('tstar.txt', 'a') as f:
            f.write(txt)
            f.write('\n')
