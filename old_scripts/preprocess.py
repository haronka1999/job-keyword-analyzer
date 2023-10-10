import re
import string
from resources.constants import CONTRACTION_MAP
import nltk
from nltk.tokenize import ToktokTokenizer
import num2words
import inflect

tokenizer = ToktokTokenizer()
stopword_list = nltk.corpus.stopwords.words('english')


def expand_contractions(text, map=CONTRACTION_MAP):
    pattern = re.compile('({})'.format('|'.join(map.keys())), flags=re.IGNORECASE | re.DOTALL)

    def get_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded = map.get(match) if map.get(match) else map.get(match.lower())
        expanded = first_char + expanded[1:]
        return expanded

    new_text = pattern.sub(get_match, text)
    new_text = re.sub("'", "", new_text)
    return new_text


def remove_months(text):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    filtered_words = []
    # Split the text into individual words
    words = text.split()
    # Loop through each word in the text
    for word in words:
        # If the word is not in the list of words to remove, add it to the filtered list
        if word not in months:
            filtered_words.append(word)
        else:
            print(filtered_words)

    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)

    # Return the filtered text
    return filtered_text


def replace_numbers(text):
    p = inflect.engine()
    words = text.split()
    new_words = []
    for word in words:
        # If word is a number spelled out, replace it with its numerical equivalent
        if word.isalpha() and p.singular_noun(word) is False:
            num = p.number_to_words(word)
            new_words.append(p.number_to_words(word))
        else:
            new_words.append(word)
    return ' '.join(new_words)


def remove_special_characters(text):
    # define the pattern to keep
    pat = r'[^a-zA-z0-9.,!?/:;\"\'\s]'
    return re.sub(pat, '', text)


def remove_punctuation(text):
    text = ''.join([c for c in text if c not in string.punctuation])
    return text


def get_stem(text):
    stemmer = nltk.porter.PorterStemmer()
    text = ' '.join([stemmer.stem(word) for word in text.split()])
    return text


def remove_stopwords(text):
    # convert sentence into token of words
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    # check in lowercase
    t = [token for token in tokens if token.lower() not in stopword_list]
    text = ' '.join(t)
    return text


def remove_numbers(text):
    return re.sub(r'\d+', '', text)


def remove_extra_whitespace_tabs(text):
    # pattern = r'^\s+$|\s+$'
    pattern = r'^\s*|\s\s*'
    return re.sub(pattern, ' ', text).strip()
