# LinkedIn Job Post Analysis Tool

A Python application that scrapes LinkedIn job postings, preprocesses text data, extracts keywords using multiple NLP methods, and generates word cloud visualizations.

**Note:** This project showcases traditional NLP capabilities using established libraries and techniques. It does not use modern Large Language Models (LLMs) like GPT, Claude, or similar generative AI models.

## Features

- Web scraping of LinkedIn job postings using Selenium
- Automatic language detection and translation to English
- Text preprocessing (contraction expansion, special character removal, etc.)
- Multiple keyword extraction methods:
  - KeyBERT (BERT-based keyword extraction)
  - spaCy (Named Entity Recognition)
  - YAKE (Yet Another Keyword Extractor)
  - RAKE (Rapid Automatic Keyword Extraction)
- Word cloud generation for visualization
- YAML-based configuration

## Installation

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd job-keyword-analyzer
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLP resources:
```bash
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader punkt
python3 -m spacy download en_core_web_sm
python3 -m spacy download en_core_web_lg
```

## Usage

### Configuration

Create a `config/input.yaml` file with your search parameters:

```yaml
data_source:
  mode: "scrape"  # or "existing" to use saved job descriptions
  file_path: "data/raw/job_descriptions.txt"

scraping:
  job_title: "Python Developer"
  location: "united states"  # Just specify the location name!

keyword_extraction:
  methods: ["keybert", "spacy", "yake", "rake"]

word_cloud:
  enabled: true    # Requires spacy in keyword_extraction methods
  display: false   # Set to true to display the word cloud
```

### Location Configuration

The application includes a **built-in geo ID database** with 50+ countries and regions. Simply specify the location name (case-insensitive):

```yaml
scraping:
  location: "united states"  # or "USA", "us" - all work!
  location: "germany"        # lowercase works
  location: "United Kingdom" # any case works
```

#### Supported Locations

The database includes 50+ locations:

**North America:** United States, Canada, Mexico

**Europe:** United Kingdom, Germany, France, Spain, Italy, Netherlands, Switzerland, Sweden, Norway, Denmark, Belgium, Austria, Poland, Ireland, Portugal, Greece, Czech Republic, Romania, Hungary, Finland

**Asia Pacific:** Australia, India, China, Japan, Singapore, South Korea, Hong Kong, New Zealand, Indonesia, Malaysia, Thailand, Philippines, Vietnam, Taiwan

**Middle East & Africa:** United Arab Emirates, Saudi Arabia, Israel, South Africa, Egypt, Nigeria, Kenya

**South America:** Brazil, Argentina, Chile, Colombia, Peru

**Common Aliases:** usa, us, uk, uae (all supported)

To see the complete list, check `src/linkedin_job_analysis/config/geo_database.py` or run:

```python
from src.linkedin_job_analysis.config.geo_database import list_available_locations
print('\n'.join(list_available_locations()))
```

#### Fuzzy Matching

The system includes smart typo correction:

```yaml
location: "germny"  # Suggests: "Did you mean: germany?"
location: "untied states"  # Suggests: "Did you mean: united states?"
```

#### Adding Custom Locations

If you need a location not in the database:

1. Find the LinkedIn geo ID using browser developer tools (see section below)
2. Add it to `src/linkedin_job_analysis/config/geo_database.py`:

```python
GEO_DATABASE = {
    # ... existing entries ...
    "berlin, germany": "106967730",  # Add your custom location
}
```

3. Use lowercase for the key name

**Note:** All keys in the database are lowercase, and all lookups are case-insensitive.

### Finding LinkedIn Geo IDs (For Custom Locations)

If you need to add a location not in the database, find its geo ID:

#### Method 1: Browser Developer Tools

1. Go to [LinkedIn Job Search](https://www.linkedin.com/jobs/)
2. Open Developer Tools (F12 or Right-click → Inspect)
3. Go to the **Network** tab
4. Click on the location filter and select your desired location
5. Look for API requests containing "typeahead" or "geo"
6. Find the geo ID like `"id": "103644278"` or `"geoUrn": "urn:li:geo:103644278"`

#### Method 2: From URL

LinkedIn job search URLs contain the geo ID:
```
https://www.linkedin.com/jobs/search/?geoId=103644278&keywords=...
```

### Running the Application

Simply run the main script:

```bash
python main.py
```

The application will read your configuration from `config/input.yaml` and execute the analysis workflow.

## Data Flow

1. Job descriptions are scraped from LinkedIn or loaded from existing file
2. Raw text undergoes preprocessing:
   - Lowercase normalization
   - Contraction expansion
   - Special character removal
   - Punctuation removal
   - Whitespace normalization
3. Preprocessed text is saved to `data/processed/`
4. Keywords are extracted using selected methods
5. Results are saved to `data/results/`
6. Word clouds are generated and saved to `data/images/`
