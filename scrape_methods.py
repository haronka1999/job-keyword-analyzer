import time
import traceback

import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from langdetect import detect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from resources.constants import (
    MAX_SCROLL_ATTEMPTS,
    PAGE_LOAD_TIMEOUT,
    REQUEST_DELAY,
    REQUEST_TIMEOUT,
    SCROLL_DELAY,
)

"""
This file is related to job description scraping
"""


def get_job_description_url_list(postings_name, country, country_geo_id):
    """
    Scrape LinkedIn job posting URLs using Selenium.

    Args:
        postings_name (str): Job title to search for
        country (str): Country name for the search
        country_geo_id (str): LinkedIn geographic ID for the country

    Returns:
        list: List of job posting URLs found, empty list if driver initialization fails
    """
    # building linkedin link
    posit = "%20".join(postings_name.split())
    url = f"https://www.linkedin.com/jobs/search?keywords={posit}&location={country}&geoId={country_geo_id}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"

    # Tracks the number of scroll attempts to load more job postings
    numb_refresh_page = 0

    # opening url in Chrome browser
    print("Creating webdriver ... ")
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("detach", True)
        options.add_argument("headless")
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, PAGE_LOAD_TIMEOUT)
        driver.get(url)
        previous_height = driver.execute_script("return document.body.scrollHeight")
    except Exception as e:
        print("[ERROR] Failed to initialize Selenium WebDriver.")
        print("Please ensure Chrome and ChromeDriver are installed:")
        print("  - Install Chrome: https://www.google.com/chrome/")
        print("  - Install ChromeDriver: https://chromedriver.chromium.org/")
        print(f"Exception: {type(e).__name__}: {str(e)}")
        return []

    print("Retrieving job posts URLs ...")

    try:
        while True:
            # scrolling to the bottom of body height (y coordinate)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # pausing to load more content
            time.sleep(SCROLL_DELAY)
            # assigning webpage's increased body height in pixels
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == previous_height:
                next_page_button = wait.until(
                    expected_conditions.element_to_be_clickable(
                        (By.CLASS_NAME, "infinite-scroller__show-more-button")
                    )
                )
                next_page_button.click()
                numb_refresh_page += 1
                if numb_refresh_page == MAX_SCROLL_ATTEMPTS:
                    break

            # updating previous height for the next loop
            previous_height = new_height
        print("Job posts retrieved.")

        links = driver.find_elements(By.CLASS_NAME, "base-card__full-link")
        links_list = [link.get_attribute("href") for link in links]

        print("Number of links created " + str(len(links_list)))
        return links_list
    finally:
        driver.quit()


def scrape_job_description(links_list):
    """
    Scrape job descriptions from a list of LinkedIn URLs.

    Fetches each URL, extracts job description text, detects language,
    and translates non-English descriptions to English.

    Args:
        links_list (list): List of LinkedIn job posting URLs to scrape

    Returns:
        list: List of job description texts (only non-empty descriptions)
    """
    job_description_list = []
    counter = 1
    # looping through the links
    for link in links_list:
        job_description = ""
        try:
            # Network request with error handling
            request = requests.get(link, timeout=REQUEST_TIMEOUT)
            print(str(counter) + ". " + str(request))
            soup = BeautifulSoup(request.text, "lxml")

            # Extract text based on CSS class
            job_description = soup.find(
                "div", class_="show-more-less-html__markup"
            ).get_text(separator=" ")

            lang = detect(job_description)
            # Translate to English
            if lang != "en":
                print("Translation incoming from language: " + str(lang))
                try:
                    translator = Translator()
                    job_description = translator.translate(
                        job_description, src=lang, dest="en"
                    ).text
                except Exception as translation_error:
                    print(
                        f"[WARNING] Translation failed: {translation_error}. "
                        "Using original text."
                    )
        except requests.exceptions.RequestException as e:
            print("ERROR! Network request failed.")
            print("Exception:", type(e).__name__)
            print("Exception details:", str(e))
        except AttributeError as e:
            print("ERROR! Failed to find the desired element.")
            print("Exception:", type(e).__name__)
            print("Exception details:", str(e))
            traceback.print_exc()
        except Exception as e:
            print("ERROR! In retrieving data...")
            print("Exception:", type(e).__name__)
            print("Exception details:", str(e))

        # Clean and append job description (skip if empty)
        if job_description:
            job_description = job_description.replace("\n", " ")
            job_description_list.append(job_description)

        # Pausing to avoid error 429
        time.sleep(REQUEST_DELAY)
        counter += 1
    return job_description_list
