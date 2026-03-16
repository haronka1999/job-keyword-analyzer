"""Main entry point for Job Keyword Analyzer."""

import os

from src.linkedin_job_analysis.config.geo_database import get_geo_id
from src.linkedin_job_analysis.config.loader import load_config
from src.linkedin_job_analysis.config.settings import WORDCLOUD_KEYWORD_SOURCE
from src.linkedin_job_analysis.extraction import extractors
from src.linkedin_job_analysis.preprocessing.pipeline import preprocess_data
from src.linkedin_job_analysis.scraping.linkedin_scraper import (
    get_job_description_url_list,
    scrape_job_description,
)
from src.linkedin_job_analysis.visualization.wordcloud import generate_wordcloud


def scrape_new_jobs(config, file_path):
    """Scrape new job descriptions from LinkedIn."""
    scraping_config = config["scraping"]
    job_title = scraping_config["job_title"]
    location = scraping_config["location"]

    print("\n[INFO] Starting job scraping process...")

    # Lookup geo ID from location name
    try:
        country_geo_id = get_geo_id(location)
        print(f"[INFO] Location: {location} (Geo ID: {country_geo_id})")
    except ValueError as e:
        print(f"[ERROR] {e}")
        return None, None

    print(f"[INFO] Searching for '{job_title}' positions in {location}")

    link_list = get_job_description_url_list(job_title, location, country_geo_id)
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
    preprocessed_jd = preprocess_data(job_description_string)
    print("[INFO] Preprocessing complete")
    return preprocessed_jd


def extract_keywords(preprocessed_jd, methods):
    """Extract keywords using selected methods."""
    print("\n--- Keyword Extraction ---")
    keywords_dict = {}

    for method in methods:
        print(f"\n[INFO] Extracting keywords using {method.upper()}...")

        if method == "keybert":
            keywords = extractors.get_keywords_by_keybert(preprocessed_jd)
            keywords_dict["keybert"] = keywords

        elif method == "spacy":
            keywords = extractors.get_keywords_by_spacy(preprocessed_jd)
            keywords_dict["spacy"] = keywords

        elif method == "yake":
            extractors.get_keywords_by_yake(preprocessed_jd)
            print("[INFO] YAKE results displayed above")

        elif method == "rake":
            extractors.get_keywords_by_rake(preprocessed_jd)
            print("[INFO] RAKE results saved to data/results/rake_nltk.txt")

    return keywords_dict


def main():
    """Main function that orchestrates the job analysis workflow."""
    print("\n" + "=" * 60)
    print("Job Keyword Analyzer")
    print("=" * 60 + "\n")

    config = load_config()

    data_source_mode = config["data_source"]["mode"]
    file_path = config["data_source"]["file_path"]

    job_description_list = None
    job_title = "Job"

    if data_source_mode == "scrape":
        job_description_list, job_title = scrape_new_jobs(config, file_path)
        if job_description_list is None:
            print("[ERROR] Scraping failed. Please check the location configuration.")
            return
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

    if not job_description_list:
        print("[ERROR] No job descriptions found. Cannot proceed with analysis.")
        return

    preprocessed_jd = preprocess_jobs(job_description_list)

    methods = config["keyword_extraction"]["methods"]
    print(f"[INFO] Using keyword extraction methods: {', '.join(methods)}")
    keywords_dict = extract_keywords(preprocessed_jd, methods)

    word_cloud_config = config.get("word_cloud", {})
    if word_cloud_config.get("enabled", False):
        if (
            WORDCLOUD_KEYWORD_SOURCE in keywords_dict
            and keywords_dict[WORDCLOUD_KEYWORD_SOURCE]
        ):
            display = word_cloud_config.get("display", False)
            generate_wordcloud(
                keywords_dict[WORDCLOUD_KEYWORD_SOURCE],
                job_title,
                len(job_description_list),
                display,
            )
        else:
            print(
                f"[WARNING] Word cloud generation requires '{WORDCLOUD_KEYWORD_SOURCE}'"
                f"method. Please add '{WORDCLOUD_KEYWORD_SOURCE}'"
                f"to keyword_extraction methods in config/input.yaml"
            )

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
