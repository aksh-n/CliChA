"""This module contains a helper class to format and write text into files.

This module is NOT a direct part of scrapy.
"""

import logging
import sys
from io import FileIO


class TextWriter:
    # count the number of articles 
    counter: int
    _file: FileIO

    def __init__(self, file_path: str) -> None:
        # overwrite the file instead of appending to it
        # encoding has to be manually set to bypass Windows locale settings
        self.counter = 0
        self._file = open(file_path, 'w', encoding='utf-8', errors='ignore')
    
    def append_article(self, body: str) -> None:
        try:
            self._file.write(str(self.counter) + '-> ' + body)
            self._file.write('\n--------\n')

            self.counter += 1
        except IOError:
            logging.error('An error occurred! Terminating.')
            sys.exit(-1)

    def close(self) -> None:
        self._file.write('Articles crawled: ' + str(self.counter) + '\n')
        self._file.close()

    def __del__(self):
        if not self._file.closed:
            self._file.close()


# TODO Remove this 
def append_article(file_path: str, body: str):
    """Append an article to the file specified by file_path."""

    # encoding has to be manually set to bypass Windows locale settings
    with open(file_path, 'a', encoding='utf-8', errors="ignore") as f:
        f.write(body)
        f.write('\n--------\n')
