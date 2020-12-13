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


def articles_process_yearly(dataset_name: str, year_start: int, year_end: int,
                            attribute: str = "LOWER") -> None:
    """Processes dataset_name articles and writes a report for each year separately from year_start
    to year_end (both inclusive) in climate_data/{dataset_name}_processed_data.

    Instance Attributes:
        - dataset_name: the name of the dataset (for ex: 'nytimes', 'science_daily_small')
        - year_start: the year to start processing from
        - year_end: the year to end processing on
        - attribute: the attribute to be passed to the function phrase_matcher
        Useful options for attribute are 'LOWER' and 'LEMMA'

    For each row in {year}.txt in climate_data/{dataset_name}_processed_data,
    row[0] is the index of the article
    row[1] is the number of distinct keywords matched in that article
    row[2] is the total number of keywords matched in that article
    row[3] is a list of (keyword, number of times keyword occurred) pairs of that article 

    CAUTION: Passing 'LEMMA' as the attribute on the entirety of one of the datasets will cause the
    function to process for many hours (perhaps a day), and may even terminate in case RAM is
    overloaded and/or has limited capacity.
    In comparison, passing 'LOWER' as the attribute on the entirety of one of the datasets will
    cause the function to complete within an hour or two.
    """
    idf_dict = create_idf_dict()
    matcher = sh.phrase_matcher(KEYWORDS, attribute)
    for year in range(year_start, year_end + 1):
        filename = f"clicha_scrapy/{dataset_name}/{year}.txt"
        if attribute != "LOWER":
            docs = sh.list_doc_from_text(filename, tagging=True)
        else:
            docs = sh.list_doc_from_text(filename)
        articles_with_matches = []
        for i, doc in enumerate(docs):
            total_matches, distinct_matches, counter_items = sh.phrase_matching(doc, matcher)
            article_cai = article_climate_awareness_index(counter_items, idf_dict, len(doc))
            if distinct_matches > 0:
                articles_with_matches.append(
                    [i, distinct_matches, total_matches, article_cai, counter_items]
                )
        articles_with_matches.sort(key=lambda x: x[1], reverse=True)
        with open(f'climate_data/{dataset_name}_processed_data/{year}.txt', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(articles_with_matches)


def article_climate_awareness_index(matches: list, idf_dict: dict, length_of_doc: int) -> float:
    """Returns a numeric estimate of how climate aware a Doc is.
    A Doc (a sequence of Tokens) is a class in spaCy.

    Instance Attributes:
        - matches: a list of tuples consisting of a word and the number of times it occurred
        - idf_dict: an idf (Inverse Document Frequency) dict
        - length_of_doc: the length of the given Doc (an article can be a Doc)
    """
    article_cai = 0
    for word, count in matches:
        if word in idf_dict:
            article_cai += idf_dict[word] * count
        else:
            article_cai += 10 * count
    if length_of_doc == 0:
        length_of_doc = 1
    return round(article_cai / length_of_doc, 5)


def articles_process(dataset_name: str, year_start: int, year_end: int) -> None:
    """Prepares a cumulative report about climate_change for all the years from year_start
    to year_end (both inclusive) on a given dataset, in a csv file.

    Instance Attributes:
        - dataset_name: the name of the dataset (for ex: 'nytimes', 'science_daily_small')
        - year_start: the year to start processing from
        - year_end: the year to end processing on

    For each row in the csv file,
    row[0] is the year
    row[1] is the number of articles which tested climate-change positive
    row[2] is the Climate Awareness Index of that year
    row[3] is the total number of articles processed for that year
    """
    with open(f'climate_data/{dataset_name}_climate_change_data.txt', 'w') as f:
        writer = csv.writer(f)
        for year in range(year_start, year_end + 1):
            filename = f"climate_data/{dataset_name}_processed_data/{year}.txt"
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
    # articles_process("nytimes", 1851, 2020)
    #
    # WARNING: The above code may take more than hour to process and with the LEMMA attribute,
    # it may take an entire day. 
    # Hence, the processesing has already been done in advance (with the LEMMA attribute).
    # Running the above code will overwrite the previous data processing done by LEMMA attribute which
    # is slightly more accurate (but much more time consuming) than the default LOWER attribute.
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['spaCy_helpers', 'find_climate_keywords', 'csv'],
    #     'allowed-io': ['articles_process_yearly', 'articles_process', 'test_climate_aware'],
    #     'max-line-length': 100,
    #     'max-locals': 25,
    #     # E9997: The h when using 'with open(...) as h' is a lowercase letter by convention.
    #     'disable': ['R1705', 'C0200', 'E9997']
    # })
    pass