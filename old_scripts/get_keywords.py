import spacy
import yake
import nltk
from keybert import KeyBERT
import unicodedata
import preprocess
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def read_jobs():
    with open('../resources/job_descriptions.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Remove newline characters from each line
    lines = [line.strip() for line in lines]
    job_descriptions = [element for element in lines if element.strip()]
    return ' '.join(job_descriptions)


def preprocess_data(jobs):
    # remove accented characters
    jobs = unicodedata.normalize('NFKD', jobs).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    jobs = preprocess.expand_contractions(jobs)
    jobs = preprocess.remove_special_characters(jobs)
    jobs = preprocess.remove_punctuation(jobs)
    # jobs = preprocess.get_stem(jobs)
    jobs = preprocess.remove_punctuation(jobs)
    # jobs = preprocess.replace_numbers(jobs)
    # jobs = preprocess.remove_months(jobs)
    jobs = preprocess.remove_extra_whitespace_tabs(jobs)
    # jobs = preprocess.remove_numbers(jobs)
    f = open("outpt_text.txt", "w", encoding='utf-8')
    f.write(jobs)
    f.close()
    return jobs


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


jobs_string = read_jobs()
jobs_string = preprocess_data(jobs_string)

print("spacy:")
keywords = get_keywords_by_spacy(jobs_string)

wordcloud = WordCloud(width=800, height=800,
                      background_color='black',
                      stopwords=nltk.corpus.stopwords.words('english'),
                      min_font_size=10
                      ).generate(' '.join(keywords))


# plotting the WordCloud image with matplotlib``
plt.figure(figsize=(10, 10), facecolor='Black')
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

# assigning file path
p_name = '_'.join('Java'.split())
f_path = f'{p_name}-{100}_c.png'
# saving png
plt.savefig(f_path)
# printing the plot
plt.show()


