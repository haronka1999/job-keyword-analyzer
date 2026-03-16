import spacy
import yake
from keybert import KeyBERT
from rake_nltk import Rake

"""
RESPONSIBLE FOR APPLYING LANGUAGE MODELS TO THE PREPROCESSED TEXT
"""


def get_keywords_by_spacy(jobs):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(jobs)
    keywords = []
    for ent in doc.ents:
        keywords.append(ent.text)
        print(ent.text, ent.label_)
    return keywords


def get_keywords_by_yake(jobs):
    max_ngram_size = 3
    deduplication_threshold = 0.7
    num_of_keywords = 20
    custom_kw_extractor = yake.KeywordExtractor(
        lan="en",
        n=max_ngram_size,
        dedupLim=deduplication_threshold,
        top=num_of_keywords,
        features=None,
    )
    keywords = custom_kw_extractor.extract_keywords(jobs)
    for kw in keywords:
        print(kw)


def get_keywords_by_keybert(jobs):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(
        jobs, keyphrase_ngram_range=(1, 2), stop_words="english"
    )
    for i in keywords:
        print(i)


def get_keywords_by_rake(text):
    r = Rake(min_length=1, max_length=3, include_repeated_phrases=False)
    r.extract_keywords_from_text(text)
    with open("resources/rake_nltk.txt", "w") as file:
        for rating, keyword in r.get_ranked_phrases_with_scores():
            if rating > 5:
                file.write(f"({keyword}, {rating})\n")
    print("The Rake tuples  has been saved to resources/rake_nltk")
