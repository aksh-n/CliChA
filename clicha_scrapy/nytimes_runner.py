"""Climate Change Awareness (CliChA), NYTimes Runner

This module was used to run the NYTimesTextSpider to collect the data. It should not be imported
or run anywhere other than as a top level script.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
import os
from sys import argv

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
        'max-line-length': 99,
        'max-args': 5,
        'max-locals': 24,
        # W0220: by the documentation, parse does not need **kwargs
        # W0612: 'closed' is called by Scrapy, requiring the 'reason' argument
        'disable': ['R1704', 'W0221', 'W0613'],
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    # -----------------------------------------------------------
    # the actual code

    start = int(argv[1])
    end = int(argv[2])

    for i in range(start, end, 5):
        print('Starting job ' + str(i))
        os.system(
            f'scrapy crawl nytimestext -a start={i} -a end={i+4} --logfile ".\\nytimeslog\\{i}.txt"'
        )
