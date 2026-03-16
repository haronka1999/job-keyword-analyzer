"""Text cleaning functions for preprocessing job descriptions."""

import re


def expand_contractions(text, contraction_mapping):
    """Expand contractions in text using the provided mapping.

    Args:
        text: Input text string
        contraction_mapping: Dictionary mapping contractions to expansions

    Returns:
        Text with contractions expanded
    """
    contractions_pattern = re.compile(
        "({})".format("|".join(contraction_mapping.keys())),
        flags=re.IGNORECASE | re.DOTALL,
    )

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = (
            contraction_mapping.get(match)
            if contraction_mapping.get(match)
            else contraction_mapping.get(match.lower())
        )
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text


def remove_special_characters(text):
    """Remove special characters from text,
        keeping only alphanumeric and basic punctuation.

    Args:
        text: Input text string

    Returns:
        Text with special characters removed
    """
    text = re.sub(r"[^a-zA-z0-9\s.,!?]", "", text)
    return text


def remove_punctuation(text):
    """Remove punctuation from text.

    Args:
        text: Input text string

    Returns:
        Text with punctuation removed
    """
    text = re.sub(r"[.,!?;:\'\"-]", "", text)
    return text


def remove_extra_whitespace_tabs(text):
    """Remove extra whitespace and tabs from text.

    Args:
        text: Input text string

    Returns:
        Text with normalized whitespace
    """
    text = re.sub(r"[\t\n\r]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
