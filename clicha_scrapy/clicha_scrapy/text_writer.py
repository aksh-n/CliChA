"""This module contains helper functions to format and write text into files.

This module is NOT a direct part of scrapy.
"""

def append_article(file_path: str, body: str):
    """Append an article to the file specified by file_path."""

    # encoding has to be manually set to bypass Windows locale settings
    with open(file_path, 'a', encoding='utf-8', errors="ignore") as f:
        f.write(body)
        f.write('\n--------\n')
