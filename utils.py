import os
import unicodedata

import preprocess
from resources.constants import OUTPUT_DIR, PREPROCESSED_TEXT_FILE

"""
Here comes every utility function
"""


def preprocess_data(jobs):
    """
    Preprocess job description text.

    Applies multiple text cleaning operations including accent removal,
    contraction expansion, special character removal, punctuation removal,
    and whitespace normalization. Saves preprocessed text to file.

    Args:
        jobs (str): Raw job description text

    Returns:
        str: Preprocessed text
    """
    # MANDATORY PREPROCESS:

    # remove accented characters
    jobs = (
        unicodedata.normalize("NFKD", jobs)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
    )
    jobs = preprocess.expand_contractions(jobs)
    jobs = preprocess.remove_special_characters(jobs)
    jobs = preprocess.remove_punctuation(jobs)
    jobs = preprocess.remove_extra_whitespace_tabs(jobs)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(PREPROCESSED_TEXT_FILE, "w", encoding="utf-8") as f:
        f.write(jobs)
    return jobs
