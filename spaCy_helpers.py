import spacy
from pprint import pprint
from collections import Counter
from math import log

stop_list = ["Mr.", "Ms.", "Mrs.", "say", "'s", "Dr."]
nlp = spacy.load('en_core_web_sm', disable=["tagger","parser", "ner"])
phrase_nlp = spacy.load('en_core_web_sm', disable=["ner"])
nlp.Defaults.stop_words.update(stop_list)
phrase_nlp.Defaults.stop_words.update(stop_list)


def doc_from_text(filename: str) -> spacy.tokens.Doc:
    """Returns a Doc object from the text in filename."""
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        # text = f.read().decode(encoding=encoding) - takes encoding as parameter
        text = f.read()
    doc = nlp(text)
    return doc


def list_doc_from_text(filename: str, num: int=-1, tagging=False) -> spacy.tokens.Doc:
    """Returns a list of first num Doc objects from the text in filename.
    
    If num is None, then all Doc objects from the text are returned.
    """
    with open(filename, 'r') as f:
        texts = f.read().split("--------")
    if num != -1:
        texts = texts[:num]
    else: 
        num = len(texts)
    if tagging:
        docs = []
        for i in range((num // 100) + 1):  # to prevent excess memory consumption and termination of task.
            docs += list(phrase_nlp.pipe(texts[i * 100: (i + 1) * 100]))
    else:
        docs = list(nlp.pipe(texts))
    return docs


def term_frequency_dict(doc: spacy.tokens.Doc) -> dict:
    """Returns a dict of the term frequency of each term in the given doc.

    Term Frequency(t) = number of times term t appears in a document / the total number of terms in the document"""
    words = [preprocess_token(token) for token in doc if is_token_allowed(token)]
    count = Counter(words)
    return {word: count[word] / len(words) for word in count}


def inverse_document_frequency_dict(tf_dicts: list) -> dict:
    """Returns a dict of inverse document frequency of each term.
    tf_dicts is the list in which each element is a term_frequency_dict of a single doc.

    Inverse Document Frequency(t) = log_e(Total number of documents/ Number of documents with term t in it)"""
    words = Counter()  # Dict of all the words occuring in at least one of the documents
    for tf_dict in tf_dicts:
        words = words + Counter(tf_dict.keys())
    return {word: log(len(tf_dicts) / words[word]) for word in words}


def tf_idf(term: str, tf_dict: dict, idf_dict: dict) -> float:
    """Returns the tf-idf (Term Frequency-Inverse Document Frequency) of a term in a document.
    tf_dict is a term_frequency_dict of a single doc.
    idf_dict is a inverse_document_frequency_dict.

    tf-idf(t)  = Term Frequency(t) * Inverse Document Frequency(t)"""
    if term not in idf_dict:
        return 1000
    return tf_dict[term] * idf_dict[term]


def tf_idf_dict(tf_dict: dict, idf_dict: dict) -> dict:
    """Returns a dict in which each key is a term mapping to tf-idf(term).
    tf_dict is a term_frequency_dict of a single doc.
    idf_dict is a inverse_document_frequency_dict."""
    tf_idf_dict = {}
    for term in tf_dict.keys():
        tf_idf_dict[term] = tf_idf(term, tf_dict, idf_dict)
    return tf_idf_dict


def highest_tf_idf(tf_dict: dict, idf_dict: dict) -> list:
    """Returns a list in which each element is a tuple of term and tf-idf(term).
    tf_dict is a term_frequency_dict of a single doc.
    idf_dict is a inverse_document_frequency_dict."""
    tf_idf_list = []
    for term in tf_dict.keys():
        tf_idf_list.append((term, tf_idf(term, tf_dict, idf_dict)))
    tf_idf_list.sort(key=lambda x: x[1], reverse=True)
    return tf_idf_list


def set_custom_boundaries(doc: spacy.tokens.Doc) -> None:
    """Sets is_sent_start of each token after ellipses to True in doc."""
    for token in doc[:-1]:
        if token.text == '...':
            doc[token.i + 1].is_sent_start = True
    return doc


def sentence_detect(doc: spacy.tokens.Doc) -> list:
    """Returns a list of sentences in the given file."""
    return list(doc.sents)


def lemmatization(doc: spacy.tokens.Doc) -> list:
    """Returns a list of tuples having a (non-stop) word and lemmatized version of it, present in the given file."""
    return [(token, token.lemma_) for token in doc if not token.is_stop and not token.is_punct]


def frequency_words(doc: spacy.tokens.Doc, n: int = None) -> Counter:
    """Returns a list of n (non-stop) words that are the most common in the given file."""
    words = [preprocess_token(token) for token in doc if is_token_allowed(token)]
    if n is None:
        return Counter(words)
    return Counter(words).most_common(n)


def all_pos_explained(doc: spacy.tokens.Doc) -> list:
    "Returns a list of each token in the given file along with its pos, pos_ attributes explained."
    words_explained = [(token, token.pos, token.pos_, spacy.explain(token.pos_)) for token in doc]
    return words_explained


def pos_words(doc: spacy.tokens.Doc, pos: str) -> set:
    """Returns a set of the given pos (Part-of-Speech) words"""
    return {token for token in doc if token.pos_ == pos}


def is_token_allowed(token: spacy.tokens.Token) -> bool:
    """Returns whether token is allowed or not. Allowed tokens are all tokens except stop words, punctuations and whitespace(s)."""
    return not (not token.text.strip() or token.is_stop or token.is_punct)


def preprocess_token(token: spacy.tokens.Token) -> str:
    """Returns the lowercased lemmatized version of the token."""
    return token.lemma_.strip().lower()


def phrase_matching(doc: spacy.tokens.Doc, terms: list, attribute: str="LOWER") -> tuple:
    """Returns a tuple containing number of matches (int) and a Counter object representing the number of times each term appears in the given doc."""
    matcher = spacy.matcher.PhraseMatcher(nlp.vocab, attr=attribute)  # attr="LEMMA" or "LOWER"
    # NOTE: make_doc is *only* a tokenizer, no processing like tagging, parsing, other labeling (like ner), etc. takes place.
    if attribute != "LOWER":
        patterns = [phrase_nlp(term) for term in terms]  # OR: patterns = list(nlp.tokenizer.pipe(terms)) - is faster for more terms
    else:
        patterns = [nlp(term) for term in terms]
    matcher.add("TerminologyList", None, *patterns)  # Instead of None, you can use an on_match callback. (eg: print("WE HAVE ATLEAST ONE MATCH WOOHOO"))
    matches = matcher(doc)
    return len(matches), Counter(preprocess_token(token) for _, start, end in matches for token in doc[start:end])
    