import unicodedata

import preprocess

"""
Here comes every utility function
"""


def preprocess_data(jobs):
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

    with open("resources/preprocessed_text.txt", "w", encoding="utf-8") as f:
        f.write(jobs)
    return jobs
