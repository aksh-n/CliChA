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
            total_matches, distinct_matches, counter_items = sh.phrase_matching(doc, keywords)
            if distinct_matches > 0:
                articles_with_matches.append([i, distinct_matches, total_matches, counter_items])
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
    with open('climate_data/climate_change_data.txt', 'w') as f:
        writer = csv.writer(f)
        for year in range(year_start, year_end + 1):
            filename = f"climate_data/test/test_{year}.txt"
            with open(filename, 'r') as f:
                data = f.readlines()
            climate_change_yearly = []
            count_climate_change = 0
            for row in data:
                distinct_keywords, total_keywords = [int(ele) for ele in row.split(',', maxsplit=3)[1:3]]
                if distinct_keywords >= 8:
                    count_climate_change += 1
            climate_change_yearly.append([year, count_climate_change, 1500])
            writer.writerows(climate_change_yearly)
    


if __name__ == "__main__":
    # for y in range(1851, 2020):
    #     nytimes_climate_test(y, y)
    nytimes_climate(1851, 2020)
