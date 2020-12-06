import os
from sys import argv
from scrapy.cmdline import execute

if __name__ == '__main__':
    start = int(argv[1])
    end = int(argv[2])

    for i in range(start, end, 5):
        print('Starting job ' + str(i))
        os.system(f'scrapy crawl nytimestext -a start={i} -a end={i+4} --logfile ".\\nytimeslog\\{i}.txt"')