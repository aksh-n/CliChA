from clicha_scrapy import demo_nytimes
from find_climate_articles import article_climate_awareness_index, create_idf_dict
import spaCy_helpers as sh

def run_demo_nytimes() -> None:
    demo_nytimes.run_spider()

def demo_processing_cai() -> list:
    """Returns a list of floats, each corresponding to a Climate Awareness Index of an article.
    
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
    pass