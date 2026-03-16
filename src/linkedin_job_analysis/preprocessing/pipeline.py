"""Text preprocessing pipeline for job descriptions."""

from ..config.settings import CONTRACTION_MAP
from .cleaners import (
    expand_contractions,
    remove_extra_whitespace_tabs,
    remove_punctuation,
    remove_special_characters,
)


def preprocess_data(data):
    """Apply complete preprocessing pipeline to text data.

    Args:
        data: Input text string

    Returns:
        Preprocessed text string
    """
    data = data.lower()
    data = expand_contractions(data, CONTRACTION_MAP)
    data = remove_special_characters(data)
    data = remove_punctuation(data)
    data = remove_extra_whitespace_tabs(data)
    return data
