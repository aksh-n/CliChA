import spaCy_helpers as sh
import spacy, csv
from pprint import pprint
from collections import Counter, defaultdict


def find_idf_tstar() -> None:
    """Writes in climate_keywords/tstar_idf.txt each term and the idf of the 
    term found in clicha_scrapy/tstar.txt"""
    docs = sh.list_doc_from_text('clicha_scrapy/tstar.txt')
    tf_dicts = [sh.term_frequency_dict(doc) for doc in docs]
    idf_dict = sh.inverse_document_frequency_dict(tf_dicts)
    with open("climate_keywords/tstar_idf.txt", "w") as f:
        writer = csv.writer(f)
        for key, val in idf_dict.items():
            writer.writerow([key, val])


def create_idf_dict() -> dict:
    """Returns the idf_dict from tstar_idf.txt"""
    with open("climate_keywords/tstar_idf.txt", "r") as f:
        reader = csv.reader(f)
        idf_dict = {}
        for term, idf in reader:
            idf_dict[term] = float(idf)
    return idf_dict


def find_possible_keywords(files: list) -> None:
    """Writes in climate_keywords/{filename}_keywords.txt rows of 3 comma-separated values.
    Each row consists of term, average tf-idf of term, number of times it occured in each document."""
    idf_dict = create_idf_dict()
    combined_filename, docs = _docs_from_climate_files(files)
    tf_idf_dicts = [sh.tf_idf_dict(sh.term_frequency_dict(doc), idf_dict) for doc in docs]
    final_dict = defaultdict(lambda: [0, 0])
    for tf_idf_dict in tf_idf_dicts:
        for term, val in tf_idf_dict.items():
            final_dict[term] = [final_dict[term][0] + val, final_dict[term][1] + 1]
    processed_final_dict = {}
    for term, val in final_dict.items():
        if val[1] > 50 and '@' not in term and "http" not in term:
            processed_final_dict[term] = [val[0] / val[1], val[1]]
    items = sorted(processed_final_dict.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
    with open(f"climate_keywords/{combined_filename}keywords.txt", "w") as f:
        writer = csv.writer(f)
        for term, val in items:
            writer.writerow([term, val])


def _docs_from_climate_files(files: list) -> tuple:
    """Returns a tuple of combined_filename and docs created from the given list 
    of filenames in climate_data."""
    docs = []
    combined_filename = ""
    for filename in files:
        docs += sh.list_doc_from_text(f'clicha_scrapy/{filename}.txt')
        combined_filename += filename + "_"
    return combined_filename, docs


def final_keywords(filename: str) -> None:
    """Writes the final keywords in climate_keywords/keywords.txt"""
    # False positives are proper nouns, acronyms, other words that aren't suitable keywords because
    # their td-idf and number of occurences are much higher due to the choice of climate-change data 
    # (NASA and UN) and other words which are concatenated as phrases instead.
    false_positives = [
        "buis", '0474', '°', 'modis', 'icebridge', 'icesat-2', 'sounder',
        'giss', 'noaa', 'jpl', 'nasa', 'goddard', 'el', 'niño', 'c', 'langley',
        'caltech', 'vandenberg', 'orbiting', 'orbit', '358', 'pasadena', 'la',
        'irvine', 'spacecraft', 'icesat', 'landsat', 'spaceborne', 'mission',
        'niña', 'carbon', 'dioxide', 'sdgs', 'wmo', 'unep', 'katowice',
        'taalas', 'fao', 'gueterres', 'un', 'antónio', 'ms.', 'covid-19'
    ]
    # Concatenated words into phrases because they (almost) always came together in climate-change data.
    keywords = ['el niño', 'la niña', 'carbon dioxide']  
    with open(f"climate_keywords/{filename}.txt", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] not in false_positives:
                keywords.append(row[0])
            if len(keywords) == 100:
                break
    with open("climate_keywords/keywords.txt", "w") as f:
        for keyword in keywords:
            f.write(keyword + "\n")


def final_keywords_merger() -> None:
    """Merges the final keywords."""


if __name__ == "__main__":
    climate_files = ["un", "nasa"]
    # find_possible_keywords(climate_files)
    # find_idf_tstar()
    final_keywords("un_nasa_keywords")