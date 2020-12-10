"""Climate Change Awareness (CliChA), TextWriter

This module contains the TextWriter, a utility class that handles text formatting and
file IO for the Spiders.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
import logging
import sys
from typing import TextIO


class TextWriter:
    """A utility class that handles text formatting and file IO for the Spiders.

    Instance Attributes:
        - counter: the number of articles already written to self._file since it opened
    """
    counter: int

    # Private Instance Attributes:
    #   - _path: the path to the file
    #   - _file: the file to write to
    _path: str
    _file: TextIO

    def __init__(self, file_path: str) -> None:
        self.counter = 0
        self._path = file_path

    def append_article(self, body: str) -> None:
        """Open the assigned file if it is not yet opened, and append body to it.

        A counter and an article delimiter are written to file along with each article body.
        """
        # don't open file until first use
        if not hasattr(self, '_file'):
            # encoding has to be manually set to bypass Windows locale settings
            self._file = open(self._path, 'a', encoding='utf-8', errors='ignore')

        try:
            self._file.write(str(self.counter) + '-> ' + body)
            self._file.write('\n--------\n')

            self.counter += 1
        except IOError:
            logging.error('An error occurred! Terminating.')
            sys.exit(-1)

    def close(self) -> None:
        """Close the TextWriter and its associated file."""
        self._file.write('Articles crawled: ' + str(self.counter) + '\n')
        self._file.close()

    def __del__(self) -> None:
        """Closes the file if it has not been already."""
        if hasattr(self, '_file') and not self._file.closed:
            self._file.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['append_article'],
        'extra-imports': ['scrapy',
                          'scrapy.spiders',
                          'scrapy.http',
                          'scrapy.exceptions',
                          'scrapy.utils.sitemap',
                          'text_writer',
                          'clicha_scrapy.text_writer',
                          'random',
                          'typing',
                          'logging',
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
