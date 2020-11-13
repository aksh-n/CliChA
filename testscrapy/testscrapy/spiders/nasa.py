import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.http import TextResponse


class NASASpider(SitemapSpider):
    """A class used to crawl the NASA climate change site for climate change related articles."""

    name = 'NASA'
    # only search this website for articles
    allowed_domains = ['climate.nasa.gov']
    sitemap_urls = ['https://climate.nasa.gov/sitemaps/news_items_sitemap.xml']

    num_of_articles = 0


    def closed(self: "NASASpider", reason: str):
        with open('nasa.txt', 'a') as f:
            f.write('Articles crawled: ' + str(self.num_of_articles) + '\n')
        
    
    def parse(self: 'NASASpider', response: TextResponse):
        """Parse each article to extract its text."""
        title = response.xpath('//h1[contains(@class, "article_title")]/text()').get().strip()
        txtlist = response.xpath(
            '(//div[contains(@class, "wysiwyg_content")]//p | //div[contains(@class, "wysiwyg_content")]//h3)/descendant-or-self::*/text()'
        ).getall()

        txt = str.join(' ', [s.strip() for s in txtlist])

        with open('nasa.txt', 'a', encoding='utf-8') as f:
            f.write(str(self.num_of_articles) + '->' + title + '\n' + txt)
            f.write('\n--------\n')
        
        self.num_of_articles += 1
