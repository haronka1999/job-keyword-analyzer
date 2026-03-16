import re
import string

from resources.constants import CONTRACTION_MAP

"""
FUNCTIONS FOR PREPROCESSING THE DATA
"""


def expand_contractions(text, map=CONTRACTION_MAP):
    pattern = re.compile(
        "({})".format("|".join(map.keys())), flags=re.IGNORECASE | re.DOTALL
    )

    def get_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded = map.get(match) if map.get(match) else map.get(match.lower())
        expanded = first_char + expanded[1:]
        return expanded

    new_text = pattern.sub(get_match, text)
    new_text = re.sub("'", "", new_text)
    return new_text


def remove_special_characters(text):
    # define the pattern to keep
    pat = r"[^a-zA-z0-9.,!?/:;\"\'\s]"
    return re.sub(pat, "", text)


def remove_punctuation(text):
    text = "".join([c for c in text if c not in string.punctuation])
    return text


def remove_extra_whitespace_tabs(text):
    pattern = r"^\s*|\s\s*"
    return re.sub(pattern, " ", text).strip()
