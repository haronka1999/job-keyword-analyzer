import re
import string

from resources.constants import CONTRACTION_MAP

"""
FUNCTIONS FOR PREPROCESSING THE DATA
"""


def expand_contractions(text):
    """
    Expand contractions in text (e.g., "don't" -> "do not").

    Args:
        text (str): Input text with contractions

    Returns:
        str: Text with expanded contractions
    """
    pattern = re.compile(
        "({})".format("|".join(CONTRACTION_MAP.keys())),
        flags=re.IGNORECASE | re.DOTALL,
    )

    def get_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded = (
            CONTRACTION_MAP.get(match)
            if CONTRACTION_MAP.get(match)
            else CONTRACTION_MAP.get(match.lower())
        )
        expanded = first_char + expanded[1:]
        return expanded

    new_text = pattern.sub(get_match, text)
    new_text = re.sub("'", "", new_text)
    return new_text


def remove_special_characters(text):
    """
    Remove special characters from text, keeping alphanumeric and basic punctuation.

    Args:
        text (str): Input text

    Returns:
        str: Text with special characters removed
    """
    # define the pattern to keep
    pat = r"[^a-zA-z0-9.,!?/:;\"\'\s]"
    return re.sub(pat, "", text)


def remove_punctuation(text):
    """
    Remove all punctuation from text.

    Args:
        text (str): Input text

    Returns:
        str: Text with punctuation removed
    """
    text = "".join(c for c in text if c not in string.punctuation)
    return text


def remove_extra_whitespace_tabs(text):
    """
    Normalize whitespace by removing extra spaces and tabs.

    Args:
        text (str): Input text

    Returns:
        str: Text with normalized whitespace
    """
    pattern = r"^\s*|\s\s*"
    return re.sub(pattern, " ", text).strip()
