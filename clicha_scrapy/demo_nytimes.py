import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ != '__main__':
    # called from root directory
    from clicha_scrapy.clicha_scrapy.spiders.nytimes import NyTimesTextSpider

def run_spider() -> None:
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'clicha_scrapy.clicha_scrapy.settings')

    settings = get_project_settings()
    settings['SPIDER_MODULES'] = ['clicha_scrapy.clicha_scrapy.spiders']
    settings['NEWSPIDER_MODULE'] = ['clicha_scrapy.clicha_scrapy.spiders']
    process = CrawlerProcess(settings)
    process.crawl(NyTimesTextSpider, demo=True, start=2020, end=2020)
    process.start()

if __name__ == '__main__':
    from clicha_scrapy.spiders.nytimes import NyTimesTextSpider