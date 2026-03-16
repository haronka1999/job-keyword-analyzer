# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Job Keyword Analyzer - A Python application that scrapes LinkedIn job postings, preprocesses the text data, extracts keywords using multiple NLP methods, and generates word cloud visualizations.

## Installation

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
# Run the main script
python main.py
```

Configuration is loaded from `config/input.yaml`.

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

The application follows a modular Python package structure with proper separation of concerns:

```
src/linkedin_job_analysis/
├── cli.py                          # Command-line interface and workflow orchestration
├── scraping/
│   └── linkedin_scraper.py        # Selenium-based LinkedIn job scraping with language detection
├── preprocessing/
│   ├── cleaners.py                # Text cleaning functions (contractions, special chars, punctuation)
│   └── pipeline.py                # Preprocessing pipeline orchestration
├── extraction/
│   └── extractors.py              # Keyword extraction (KeyBERT, spaCy, YAKE, RAKE)
├── visualization/
│   └── wordcloud.py               # Word cloud generation
├── config/
│   ├── settings.py                # Configuration constants and paths
│   ├── loader.py                  # YAML configuration loading
│   └── geo_database.py            # LinkedIn geo ID lookup database (50+ locations)
└── utils/
    └── file_io.py                 # File I/O utilities
```

## Data Flow

1. Job descriptions are scraped from LinkedIn or loaded from `data/raw/job_descriptions.txt`
2. Raw text undergoes preprocessing (normalization, contraction expansion, special character removal)
3. Preprocessed text is saved to `data/processed/preprocessed_text.txt`
4. Keywords are extracted using selected methods
5. RAKE results are saved to `data/results/rake_nltk.txt`
6. Word clouds are generated and saved to `data/images/`

## Data Directory Structure

```
data/
├── raw/              # Raw scraped job descriptions
├── processed/        # Preprocessed text files
├── results/          # Keyword extraction results
└── images/           # Generated word cloud visualizations
```

## Web Scraping Configuration

The scraping module (`src/linkedin_job_analysis/scraping/linkedin_scraper.py`) uses Selenium with headless Chrome. Configuration is loaded from `config/input.yaml`:

- `job_title`: Job title to search
- `location`: Location name (case-insensitive) - automatically looks up geo ID from built-in database
- Built-in database contains 50+ countries with fuzzy matching support
- Scrolls 10 times maximum to load additional job postings
- Includes 0.6 second delay between requests to avoid rate limiting
- Automatically translates non-English job descriptions to English

### Location Lookup System

The application includes an inline geo ID database (`config/geo_database.py`) that:
- Maps location names to LinkedIn geo IDs
- Uses all lowercase keys for consistency
- Performs case-insensitive lookups
- Includes fuzzy matching for typo correction (e.g., "germny" → suggests "germany")
- Supports 50+ countries and common aliases (usa, uk, uae)
- Easily extensible by editing the GEO_DATABASE dictionary

## Configuration File

Create `config/input.yaml` with your search parameters:

```yaml
data_source:
  mode: "scrape"  # or "existing"
  file_path: "data/raw/job_descriptions.txt"

scraping:
  job_title: "Python Developer"
  location: "united states"  # Case-insensitive, uses built-in geo database

keyword_extraction:
  methods: ["keybert", "spacy", "yake", "rake"]

word_cloud:
  enabled: true
  source: "spacy"
  display: false
```

**Location Examples:**
- `location: "united states"` or `"usa"` or `"us"`
- `location: "germany"` or `"Germany"` (case doesn't matter)
- If location not found, fuzzy matching suggests corrections

## Code Style Requirements

- Do not use emojis or arrows in code, logging, comments, or any output
- Use simple, clean text for all messages and documentation
