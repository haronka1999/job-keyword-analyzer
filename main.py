import os
import random

import matplotlib.pyplot as plt
import nltk
import yaml
from wordcloud import WordCloud

import get_keywords
import utils
from resources.constants import (
    CONFIG_FILE,
    FILENAME_RANDOM_MAX,
    FILENAME_RANDOM_MIN,
    WORDCLOUD_BG_COLOR,
    WORDCLOUD_FIGURE_SIZE,
    WORDCLOUD_HEIGHT,
    WORDCLOUD_MIN_FONT_SIZE,
    WORDCLOUD_OUTPUT_DIR,
    WORDCLOUD_WIDTH,
)
from scrape_methods import get_job_description_url_list, scrape_job_description


def load_config(config_path=CONFIG_FILE):
    """Load configuration from YAML file."""
    if not os.path.exists(config_path):
        print(f"[ERROR] Configuration file not found: {config_path}")
        print("[INFO] Please create an input.yaml file with the required configuration")
        exit(1)

    with open(config_path, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config


def print_header():
    """Print the application header."""
    print("\n" + "=" * 60)
    print("LinkedIn Job Post Analysis Tool")
    print("=" * 60 + "\n")


def scrape_new_jobs(config, file_path):
    """Scrape new job descriptions from LinkedIn."""
    scraping_config = config["scraping"]
    job_title = scraping_config["job_title"]
    country = scraping_config["country"]
    country_geo_id = scraping_config["country_geo_id"]

    print("\n[INFO] Starting job scraping process...")
    print(f"[INFO] Searching for '{job_title}' positions in {country}")

    link_list = get_job_description_url_list(job_title, country, country_geo_id)
    print(f"[INFO] Found {len(link_list)} job postings")

    job_description_list = scrape_job_description(link_list)
    job_description_list = list(set(job_description_list))

    with open(file_path, "w", encoding="utf-8") as file:
        for item in job_description_list:
            file.write(f"{item}\n")

    print(
        f"[INFO] Saved {len(job_description_list)} unique job "
        f"descriptions to {file_path}"
    )
    return job_description_list, job_title


def read_existing_jobs(file_path):
    """Read job descriptions from existing file."""
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return None

    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    job_description_list = [element for element in lines if element.strip()]

    print(
        f"[INFO] Loaded {len(job_description_list)} job descriptions from {file_path}"
    )
    return job_description_list


def preprocess_jobs(job_description_list):
    """Preprocess job descriptions."""
    print("\n[INFO] Preprocessing job descriptions...")
    job_description_string = " ".join(job_description_list)
    preprocessed_jd = utils.preprocess_data(job_description_string)
    print("[INFO] Preprocessing complete")
    return preprocessed_jd


def extract_keywords(preprocessed_jd, methods):
    """Extract keywords using selected methods."""
    print("\n--- Keyword Extraction ---")
    keywords_dict = {}

    for method in methods:
        print(f"\n[INFO] Extracting keywords using {method.upper()}...")

        if method == "keybert":
            keywords = get_keywords.get_keywords_by_keybert(preprocessed_jd)
            keywords_dict["keybert"] = keywords

        elif method == "spacy":
            keywords = get_keywords.get_keywords_by_spacy(preprocessed_jd)
            keywords_dict["spacy"] = keywords

        elif method == "yake":
            get_keywords.get_keywords_by_yake(preprocessed_jd)
            print("[INFO] YAKE results displayed above")

        elif method == "rake":
            get_keywords.get_keywords_by_rake(preprocessed_jd)
            print("[INFO] RAKE results saved to resources/rake_nltk.txt")

    return keywords_dict


def generate_wordcloud(keywords_list, job_title, num_jobs, display=False):
    """Generate and save word cloud visualization."""
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


def main():
    """Main function that reads configuration from YAML file."""
    print_header()

    config = load_config()

    data_source_mode = config["data_source"]["mode"]
    file_path = config["data_source"]["file_path"]

    job_description_list = None
    job_title = "Job"

    if data_source_mode == "scrape":
        job_description_list, job_title = scrape_new_jobs(config, file_path)
    elif data_source_mode == "existing":
        job_description_list = read_existing_jobs(file_path)
        if job_description_list is None:
            print("[ERROR] Cannot proceed without job descriptions. Exiting.")
            return
        job_title = config["scraping"].get("job_title", "Job")
    else:
        print(f"[ERROR] Invalid data source mode: {data_source_mode}")
        print("[INFO] Valid modes are: 'scrape' or 'existing'")
        return

    # Validate that we have job descriptions to process
    if not job_description_list:
        print("[ERROR] No job descriptions found. Cannot proceed with analysis.")
        return

    preprocessed_jd = preprocess_jobs(job_description_list)

    methods = config["keyword_extraction"]["methods"]
    print(f"[INFO] Using keyword extraction methods: {', '.join(methods)}")
    keywords_dict = extract_keywords(preprocessed_jd, methods)

    word_cloud_config = config.get("word_cloud", {})
    if word_cloud_config.get("enabled", False):
        source_method = word_cloud_config.get("source", "spacy")
        if source_method in keywords_dict and keywords_dict[source_method]:
            display = word_cloud_config.get("display", False)
            generate_wordcloud(
                keywords_dict[source_method],
                job_title,
                len(job_description_list),
                display,
            )
        else:
            print(
                f"[WARNING] Cannot generate word cloud: {source_method} method "
                f"not available or returned no keywords"
            )

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
