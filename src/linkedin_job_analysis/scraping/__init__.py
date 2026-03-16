"""Web scraping module for LinkedIn job postings."""

from .linkedin_scraper import (
    get_job_description_url_list,
    scrape_job_description,
)

__all__ = ["get_job_description_url_list", "scrape_job_description"]
