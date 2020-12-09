"""Climate Change Awareness (CliChA), Helper spaCy functions

This module provides spaCy helper functions, to be used for processing in other modules.

Copyright (c) 2020 Akshat Naik and Tony Hu.
Licensed under the MIT License. See LICENSE in the project root for license information.
"""
from collections import Counter
from math import log
import spacy


stop_list = ["Mr.", "Ms.", "Mrs.", "say", "'s", "Dr."]
nlp = spacy.load('en_core_web_sm', disable=["tagger", "parser", "ner"])
phrase_nlp = spacy.load('en_core_web_sm', disable=["ner"])
nlp.Defaults.stop_words.update(stop_list)
phrase_nlp.Defaults.stop_words.update(stop_list)


def doc_from_text(filename: str) -> spacy.tokens.Doc:
    """Returns a Doc object from the text in filename.

    Instance Attributes:
        - filename: the name of the file
    """
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    doc = nlp(text)
    return doc


def list_doc_from_text(filename: str, num: int = -1, tagging: bool = False) -> spacy.tokens.Doc:
    """Returns a list of the first num Doc objects from the text in filename.

    Instance Attributes:
        - filename: the name of the file
        - num: the number of Doc objects to be returned.
        if num  == -1, then all Doc objects from the text are returned
        - tagging: bool indicating whether to tag and parse the text or not
    """
    with open(filename, 'r', encoding='utf-8') as f:
        texts = f.read().split("--------")
    if num != -1:
        texts = texts[:num]
    else:
        num = len(texts)
    if tagging:
        docs = []
        # To prevent excess memory consumption and termination of task.
        for i in range((num // 100) + 1):
            docs += list(phrase_nlp.pipe(texts[i * 100: (i + 1) * 100]))
    else:
        docs = list(nlp.pipe(texts))
    return docs


def term_frequency_dict(doc: spacy.tokens.Doc) -> dict:
    """Returns a dict of the term frequency of each term in the given doc.

    Instance Attributes:
        - doc: an instance of a Doc class

    Term Frequency(t) = number of times term t appears in a document / the total number of terms in the document
    """
    words = [preprocess_token(token) for token in doc if is_token_allowed(token)]
    count = Counter(words)
    return {word: count[word] / len(words) for word in count}


def inverse_document_frequency_dict(tf_dicts: list) -> dict:
    """Returns a dict of inverse document frequency of each term.

    Instance Attributes:
        - tf_dicts: list of Term Frequency dicts, each corresponding to a single Doc.

    Inverse Document Frequency(t) = log_e(Total number of documents/ Number of documents with term t in it)
    """
    words = Counter()  # Dict of all the words occuring in at least one of the documents
    for tf_dict in tf_dicts:
        words = words + Counter(tf_dict.keys())
    return {word: log(len(tf_dicts) / words[word]) for word in words}


def tf_idf(term: str, tf_dict: dict, idf_dict: dict) -> float:
    """Returns the tf-idf (Term Frequency-Inverse Document Frequency) of a term in a document.

    Instance Attributes:
        - tf_dict: A Term Frequency dict corresponding to a single doc.
        - idf_dict: An Inverse Document Frequency dict.

    tf-idf(t) = Term Frequency(t) * Inverse Document Frequency(t)
    """
    if term not in idf_dict:
        return 1000
    return tf_dict[term] * idf_dict[term]


def tf_idf_dict(tf_dict: dict, idf_dict: dict) -> dict:
    """Returns a dict in which each key is a term mapping to tf-idf(term).

    Instance Attributes:
        - tf_dict: A Term Frequency dict corresponding to a single doc.
        - idf_dict: An Inverse Document Frequency dict.

    tf_idf_dict[t] = tf-idf(t)
    """
    tfidf_dict = {}
    for term in tf_dict.keys():
        tfidf_dict[term] = tf_idf(term, tf_dict, idf_dict)
    return tfidf_dict


def is_token_allowed(token: spacy.tokens.Token) -> bool:
    """Returns whether token is allowed or not.
    Allowed tokens are all tokens except stop words, punctuations and whitespace(s).
    """
    return not (not token.text.strip() or token.is_stop or token.is_punct)


def preprocess_token(token: spacy.tokens.Token) -> str:
    """Returns the lowercased lemmatized version of the token."""
    return token.lemma_.strip().lower()


def phrase_matching(doc: spacy.tokens.Doc, matcher: spacy.matcher.PhraseMatcher) -> tuple:
    """Returns a tuple containing number of matches (int) and a Counter object representing
    the number of times each term appears in the given doc.

    Instance Attributes:
        - doc: an instance of a Doc class
        - matcher: a PhraseMatcher object to be used for matching
    """
    matches = matcher(doc)
    counter = Counter(preprocess_token(token) for _, start, end in matches for token in doc[start:end])
    counter_items = counter.most_common()
    return len(matches), len(counter_items), counter_items


def phrase_matcher(terms: list, attribute: str = "LOWER") -> spacy.matcher.PhraseMatcher:
    """Returns a PhraseMatcher object to be used for matching in phrase_matching.

    Instance Attributes:
        - terms: a list of terms to match with
        - attribute: the Token attribute to match on
        Useful options for attribute are 'LOWER' and 'LEMMA'

    CAUTION: Passing 'LEMMA' as the attribute will cause the function runtime to increase more
    than an order of magnitude when compared to passing 'LOWER'.
    """
    matcher = spacy.matcher.PhraseMatcher(nlp.vocab, attr=attribute)  # attr="LEMMA" or "LOWER"
    if attribute != "LOWER":
        patterns = [phrase_nlp(term) for term in terms]
        # OR: patterns = list(nlp.tokenizer.pipe(terms)) - is faster for more terms
    else:
        patterns = [nlp(term) for term in terms]
    matcher.add("TerminologyList", None, *patterns)
    # Instead of None, you can use an on_match callback. (eg: print("WE HAVE ATLEAST ONE MATCH WOOHOO"))
    return matcher


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['spacy', 'collections', 'math'],
        'allowed-io': ['doc_from_text', 'list_doc_from_text'],
        'max-line-length': 120,  # writing formulae in two lines looks ugly
        'max-locals': 25,
        # C0103: The library spaCy is stylized with the 'C' being capitalized
        # E9997: nlp, phrase_nlp, stop_words, etc. are lowercase by convention according
        # to the spacy documentation.
        'disable': ['R1705', 'C0200', 'C0103', 'E9997']
    })
