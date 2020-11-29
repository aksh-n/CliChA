import spaCy_helpers as sh
import csv
from pprint import pprint

with open('climate_keywords/keywords.txt') as f:
    keywords = f.read().split('\n')


def nytimes_climate_test(year_start: int, year_end: int, attribute: str="LOWER") -> None:
    """Extracts data for testing purposes.
    """
    for year in range(year_start, year_end + 1):
        filename = f"clicha_scrapy/nytimestext/{year}.txt"
        if attribute != "LOWER":
            docs = sh.list_doc_from_text(filename, tagging=True)
        else:
            docs = sh.list_doc_from_text(filename)
        articles_with_matches = []
        for i, doc in enumerate(docs):
            matches, counter = sh.phrase_matching(doc, keywords)
            if matches > 0:
                articles_with_matches.append([i, matches, counter])
        articles_with_matches.sort(key=lambda x: x[1], reverse=True)
        with open(f'climate_data/test/test_{year}.txt', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(articles_with_matches)
        # pprint(articles_with_matches)


def nytimes_climate(year_start: int, year_end: int) -> None:
    """Calculates and writes the number of articles that tested climate-change positive 
    from year_start to year_end (both inclusive) in a csv file.
    
    For each row in the csv file,
    row[0] is the year
    row[1] is the number of articles which tested climate-change positive 
    row[2] is the total number of articles processed for that year
    """
    for year in range(year_start, year_end + 1):
        pass

if __name__ == "__main__":
    i = 0
    while 1960 + i * 10 < 2020:
        nytimes_climate_test(1960 + i * 10, 1960 + (i + 1) * 10)
        i += 1
