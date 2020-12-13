"""Climate Change Awareness (CliChA), NYTimes Demo

This module contains code to call the NyTimesTextSpider from Python code,
to be used as a demo.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ != '__main__':
    # called from root directory
    from clicha_scrapy.clicha_scrapy.spiders.nytimes import NyTimesTextSpider


def run_spider() -> None:
    """Run the NyTimesTextSpider from Python script.

    This code runs a demo version of NyTimesTextSpider and crawls articles from 2020.
    """
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'clicha_scrapy.clicha_scrapy.settings')

    settings = get_project_settings()
    settings['SPIDER_MODULES'] = ['clicha_scrapy.clicha_scrapy.spiders']
    settings['NEWSPIDER_MODULE'] = ['clicha_scrapy.clicha_scrapy.spiders']
    process = CrawlerProcess(settings)
    process.crawl(NyTimesTextSpider, demo=True, start=2020, end=2020)
    process.start()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['*'],
        'extra-imports': ['scrapy',
                          'scrapy.spiders',
                          'scrapy.http',
                          'scrapy.crawler',
                          'scrapy.utils.project',
                          'scrapy.exceptions',
                          'text_writer',
                          'clicha_scrapy.text_writer',
                          'clicha_scrapy.clicha_scrapy.spiders.nytimes',
                          'random',
                          'typing',
                          'os',
                          'sys',
                          'inspect',
                          'python_ta.contracts'],
        'max-line-length': 100,
        'max-args': 6,
        'max-locals': 25,
        # W0221: by the documentation, parse does not need **kwargs
        # W0613: 'closed' is called by Scrapy, requiring the 'reason' argument
        'disable': ['R1705', 'W0221', 'W0613'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
