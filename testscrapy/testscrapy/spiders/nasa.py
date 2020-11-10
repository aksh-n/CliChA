import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.http import TextResponse


class NASASpider(SitemapSpider):
    """A class used to crawl the NASA climate change site for climate change related articles."""
    
    name = 'NASA'
    # only search this website for articles
    allowed_domains = ['climate.nasa.gov']
    sitemap_urls = ['https://climate.nasa.gov/sitemaps/news_items_sitemap.xml']

    
    def parse(self: 'NASASpider', response: TextResponse):
        """Parse the 
        """     
        txt = str.join('', response.xpath('//div[@class="wysiwyg_content"]//p/text()').getall())

        with open('nasa.txt', 'a') as f:
            f.write(txt)
            f.write('\n')