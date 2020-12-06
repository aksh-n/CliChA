import scrapy
from scrapy.http.request import Request
from scrapy.spiders import Spider
from scrapy.http import TextResponse

if __package__ == 'clicha_scrapy.spiders':
    from clicha_scrapy.text_writer import append_article


class UNSpider(Spider):
    """A class used to crawl the NASA climate change site for climate change related articles."""

    name = 'UN'
    allowed_domains = ['news.un.org']
    num_of_articles = 0

    def closed(self, reason: str):
        with open('un.txt', 'a', encoding='utf-8') as f:
            f.write('Articles crawled: ' + str(self.num_of_articles) + '\n')

    def start_requests(self):
        base_url = 'https://news.un.org/en/news/topic/climate-change'
        
        # 51 pages in total
        for page_num in range(1, 52):
            yield Request(base_url + '?page=' + str(page_num), callback=self.parse_page)

    def parse_page(self, response: TextResponse):
        """Parse each catalog page and extract article links."""
        for each in response.xpath('//div[@class="view-content"]//h1/a/@href').getall():
            yield response.follow(each, callback=self.parse_article)

    def parse_article(self, response: TextResponse):
        """Parse each article and store its text."""
        title = response.xpath('//h1/text()').get().strip()
        body = str.join(' ', [each.strip() for each in response.xpath('(//div[@class="content"]//p | //div[@class="content"]//h3)/text()').getall()])
        if not body or body.isspace():
            return

        append_article('un.txt', str(self.num_of_articles) + '-> ' + title + '\n' + body)

        self.num_of_articles += 1
