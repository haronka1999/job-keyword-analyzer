import spacy
import yake
from keybert import KeyBERT
    
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


def get_keywords_by_YAKE(jobs):
    kw_extractor = yake.KeywordExtractor()
    max_ngram_size = 3
    deduplication_threshold = 0.7
    num_of_keywords = 20
    custom_kw_extractor = yake.KeywordExtractor(lan="en", n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=num_of_keywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(jobs)
    for kw in keywords:
        print(kw)


def get_keywords_by_KeyBERT(jobs):
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(jobs, keyphrase_ngram_range=(1, 2), stop_words='english')
    for i in keywords:
        print(i)





