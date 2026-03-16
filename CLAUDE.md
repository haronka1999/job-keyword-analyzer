# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LinkedIn Job Post Analysis Tool - A Python application that scrapes LinkedIn job postings, preprocesses the text data, extracts keywords using multiple NLP methods, and generates word cloud visualizations.

## Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the main application
python main.py
```

## Required Setup

Before first use, download necessary NLP resources:

```bash
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader punkt
python3 -m spacy download en_core_web_sm
python3 -m spacy download en_core_web_lg
```

## Dependencies

Install dependencies from requirements.txt:

```bash
pip install -r requirements.txt
```

## Architecture

The application follows a modular design with separation of concerns:

- `main.py`: Interactive CLI orchestrating the entire workflow (scraping, preprocessing, keyword extraction, visualization)
- `scrape_methods.py`: Selenium-based LinkedIn job scraping with automatic language detection and translation
- `preprocess.py`: Text preprocessing functions (contraction expansion, special character removal, punctuation handling)
- `get_keywords.py`: Keyword extraction using four NLP methods (KeyBERT, spaCy, YAKE, RAKE)
- `utils.py`: Utility functions including data reading and preprocessing pipeline
- `resources/constants.py`: Configuration constants including CONTRACTION_MAP

## Data Flow

1. Job descriptions are scraped from LinkedIn or loaded from `resources/job_descriptions.txt`
2. Raw text undergoes preprocessing (normalization, contraction expansion, special character removal)
3. Preprocessed text is saved to `resources/preprocessed_text.txt`
4. Keywords are extracted using selected methods
5. RAKE results are saved to `resources/rake_nltk.txt`
6. Word clouds are generated and saved to `resources/images/`

## Web Scraping Configuration

The scraping module uses Selenium with headless Chrome. Key parameters in `scrape_methods.py`:

- `postings_name`: Job title to search
- `country`: Country name for search
- `country_geo_id`: LinkedIn geographic ID
- Scrolls 10 times maximum to load additional job postings
- Includes 0.6 second delay between requests to avoid rate limiting
- Automatically translates non-English job descriptions to English

## Code Style Requirements

- Do not use emojis or arrows in code, logging, comments, or any output
- Use simple, clean text for all messages and documentation
