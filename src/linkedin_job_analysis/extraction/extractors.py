"""Keyword extraction using multiple NLP methods."""

import os

import spacy
import yake
from keybert import KeyBERT
from rake_nltk import Rake

from ..config.settings import (
    OUTPUT_DIR,
    RAKE_MAX_LENGTH,
    RAKE_MIN_LENGTH,
    RAKE_MIN_SCORE,
    RAKE_OUTPUT_FILE,
    SPACY_MODEL,
    YAKE_DEDUPLICATION_THRESHOLD,
    YAKE_MAX_NGRAM_SIZE,
    YAKE_NUM_KEYWORDS,
)


def get_keywords_by_spacy(jobs):
    """Extract named entities from text using spaCy.

    Args:
        jobs: Preprocessed job description text

    Returns:
        List of extracted entity texts
    """
    nlp = spacy.load(SPACY_MODEL)
    doc = nlp(jobs)
    keywords = []
    for ent in doc.ents:
        keywords.append(ent.text)
    return keywords


def get_keywords_by_yake(jobs):
    """Extract keywords using YAKE (Yet Another Keyword Extractor).

    Args:
        jobs: Preprocessed job description text

    Returns:
        List of (keyword, score) tuples
    """
    custom_kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=YAKE_MAX_NGRAM_SIZE,
        dedupLim=YAKE_DEDUPLICATION_THRESHOLD,
        top=YAKE_NUM_KEYWORDS,
        features=None,
    )
    keywords = custom_kw_extractor.extract_keywords(jobs)
    for kw in keywords:
        print(kw)
    return keywords


def get_keywords_by_keybert(jobs):
    """Extract keywords using KeyBERT (BERT-based keyword extraction).

    Args:
        jobs: Preprocessed job description text

    Returns:
        List of (keyword, relevance_score) tuples
    """
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(
        jobs, keyphrase_ngram_range=(1, 2), stop_words="english"
    )
    for i in keywords:
        print(i)
    return keywords


def get_keywords_by_rake(text):
    """Extract keywords using RAKE (Rapid Automatic Keyword Extraction).

    Saves results to a file with keywords and their scores.

    Args:
        text: Preprocessed job description text

    Returns:
        None (saves results to file)
    """
    r = Rake(
        min_length=RAKE_MIN_LENGTH,
        max_length=RAKE_MAX_LENGTH,
        include_repeated_phrases=False,
    )
    r.extract_keywords_from_text(text)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(RAKE_OUTPUT_FILE, "w") as file:
        for rating, keyword in r.get_ranked_phrases_with_scores():
            if rating > RAKE_MIN_SCORE:
                file.write(f"({keyword}, {rating})\n")
    print(f"The Rake tuples have been saved to {RAKE_OUTPUT_FILE}")
