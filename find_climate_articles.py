"""Climate Change Awareness (CliChA), Climate Change Processor

This module processes articles to calculate Climate Awareness Index (CAI)
and the number of articles that test "climate-change aware."

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
import csv
import spaCy_helpers as sh
from find_climate_keywords import create_idf_dict


with open('climate_keywords/keywords.txt') as h:
    KEYWORDS = h.read().split('\n')


def articles_process_yearly(folder: str, year_start: int, year_end: int,
                            attribute: str = "LOWER") -> None:
    """Processes folder articles and writes a cumulative report in
    climate_data/{folder}_processed_data for each year.
    """
    idf_dict = create_idf_dict()
    for year in range(year_start, year_end + 1):
        filename = f"clicha_scrapy/{folder}/{year}.txt"
        if attribute != "LOWER":
            docs = sh.list_doc_from_text(filename, tagging=True)
        else:
            docs = sh.list_doc_from_text(filename)
        articles_with_matches = []
        for i, doc in enumerate(docs):
            total_matches, distinct_matches, counter_items = sh.phrase_matching(doc, KEYWORDS)
            article_cai = article_climate_awareness_index(counter_items, idf_dict, len(doc))
            if distinct_matches > 0:
                articles_with_matches.append(
                    [i, distinct_matches, total_matches, article_cai, counter_items]
                )
        articles_with_matches.sort(key=lambda x: x[1], reverse=True)
        with open(f'climate_data/{folder}_processed_data/{year}.txt', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(articles_with_matches)


def article_climate_awareness_index(matches: list, idf_dict: dict, length_of_doc: int) -> float:
    """Returns a numeric estimate of how climate aware an article is."""
    article_cai = 0
    for word, count in matches:
        if word in idf_dict:
            article_cai += idf_dict[word] * count
        else:
            article_cai += 10 * count
    if length_of_doc == 0:
        length_of_doc = 1
    return round(article_cai / length_of_doc, 5)


def articles_process(folder: str, year_start: int, year_end: int) -> None:
    """Calculates and writes the number of articles that tested climate-change positive
    from year_start to year_end (both inclusive) in a csv file.

    For each row in the csv file,
    row[0] is the year
    row[1] is the number of articles which tested climate-change positive
    row[2] is the Climate Awareness Index of that year
    row[3] is the total number of articles processed for that year
    """
    with open(f'climate_data/{folder}_climate_change_data.txt', 'w') as f:
        writer = csv.writer(f)
        for year in range(year_start, year_end + 1):
            filename = f"climate_data/{folder}_processed_data/{year}.txt"
            with open(filename, 'r') as f:
                data = f.readlines()
            climate_change_yearly = []
            count_climate_change = 0
            year_cai = 0
            for row in data:
                row_processed = [float(ele) for ele in row.split(',', maxsplit=4)[1:4]]
                distinct_keywords, total_keywords, article_cai = row_processed
                if test_climate_aware(distinct_keywords, total_keywords, article_cai):
                    count_climate_change += 1
                if distinct_keywords >= 5:
                    year_cai += article_cai
            climate_change_yearly.append([year, count_climate_change, year_cai, 1500])
            writer.writerows(climate_change_yearly)


def test_climate_aware(distinct_keywords: float, total_keywords: float, article_cai: float) -> bool:
    """Returns whether an article with given parameters is climate aware or not."""
    return distinct_keywords >= 8 and total_keywords >= 15 and article_cai >= 0.02


if __name__ == "__main__":
    # Sample Usage (for nytimes):
    # articles_process_yearly("nytimes", 1851, 2020)
    # articles_process("nytimes", 1998, 2020)
    # WARNING: The above code may take more than hour to process.
    # Hence, the processesing has already been done in advance.
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['spaCy_helpers', 'find_climate_keywords', 'csv'],
        'allowed-io': ['articles_process_yearly', 'articles_process', 'test_climate_aware'],
        'max-line-length': 100,
        'max-locals': 25,
        'disable': ['R1705', 'C0200', 'E9997']
    })
