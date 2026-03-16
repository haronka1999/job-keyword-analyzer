"""Word cloud generation for keyword visualization."""

import os
import random

import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud

from ..config.settings import (
    FILENAME_RANDOM_MAX,
    FILENAME_RANDOM_MIN,
    WORDCLOUD_BG_COLOR,
    WORDCLOUD_FIGURE_SIZE,
    WORDCLOUD_HEIGHT,
    WORDCLOUD_MIN_FONT_SIZE,
    WORDCLOUD_OUTPUT_DIR,
    WORDCLOUD_WIDTH,
)


def generate_wordcloud(keywords_list, job_title, num_jobs, display=False):
    """Generate and save word cloud visualization.

    Args:
        keywords_list: List of keywords to include in word cloud
        job_title: Job title for filename generation
        num_jobs: Number of jobs analyzed
        display: Whether to display the plot (default: False)

    Returns:
        None (saves word cloud to file)
    """
    print("\n[INFO] Generating word cloud...")

    try:
        nltk.corpus.stopwords.words("english")
    except LookupError:
        print("[INFO] Downloading NLTK stopwords...")
        nltk.download("stopwords", quiet=True)

    wordcloud = WordCloud(
        width=WORDCLOUD_WIDTH,
        height=WORDCLOUD_HEIGHT,
        background_color=WORDCLOUD_BG_COLOR,
        stopwords=nltk.corpus.stopwords.words("english"),
        min_font_size=WORDCLOUD_MIN_FONT_SIZE,
    ).generate(" ".join(keywords_list))

    plt.figure(figsize=WORDCLOUD_FIGURE_SIZE, facecolor="Black")
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    os.makedirs(WORDCLOUD_OUTPUT_DIR, exist_ok=True)

    sanitized_job_title = "_".join(job_title.split())
    output_path = (
        f"{WORDCLOUD_OUTPUT_DIR}/{sanitized_job_title}-{num_jobs}_"
        f"{random.randint(FILENAME_RANDOM_MIN, FILENAME_RANDOM_MAX)}.png"
    )

    plt.savefig(output_path)
    print(f"[INFO] Word cloud saved to {output_path}")

    if display:
        plt.show()
    else:
        plt.close()
