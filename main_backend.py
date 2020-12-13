"""Climate Change Awareness (CliChA), Main Backend

This module contains functions that do a demo of scrapying and processing,
to be presented in the GUI program.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from clicha_scrapy import demo_nytimes
from find_climate_articles import article_climate_awareness_index, create_idf_dict
import spaCy_helpers as sh


def run_demo_nytimes() -> None:
    """Call the demo version of the NyTimesTextSpider."""
    demo_nytimes.run_spider()


def demo_processing_cai() -> list:
    """Return a list of floats, each corresponding to a Climate Awareness Index of an article.

    This is a demo processing adapted from find_climate_articles.py but in much smaller scale.
    WARNING: Run ONLY after run_demo_nytimes()
    """
    with open('climate_keywords/keywords.txt') as h:
        keywords = h.read().split('\n')
    idf_dict = create_idf_dict()
    matcher = sh.phrase_matcher(keywords)
    docs = sh.list_doc_from_text('demo_nytimes.txt')
    list_articles_cai = []
    for doc in docs:
        _, _, counter_items = sh.phrase_matching(doc, matcher)
        article_cai = article_climate_awareness_index(counter_items, idf_dict, len(doc))
        list_articles_cai.append(article_cai)
    return list_articles_cai


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['demo_processing_cai'],
        'extra-imports': [
            'clicha_scrapy',
            'find_climate_articles',
            'spaCy_helpers',
            'python_ta.contracts'
        ],
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
