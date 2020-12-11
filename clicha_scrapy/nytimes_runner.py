"""Climate Change Awareness (CliChA), NYTimes Runner

This module was used to run the NYTimesTextSpider to collect the data. It should not be imported
or run anywhere other than as a top level script.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
import os
from sys import argv

if __name__ == '__main__':
    start = int(argv[1])
    end = int(argv[2])

    for i in range(start, end, 5):
        print('Starting job ' + str(i))
        os.system(
            f'scrapy crawl nytimestext -a start={i} -a end={i+4} --logfile ".\\nytimeslog\\{i}.txt"'
        )
