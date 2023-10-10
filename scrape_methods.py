import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from langdetect import detect
from googletrans import Translator
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import traceback

"""
This file is related to job edscription scraping
"""

postings_name = 'Java'
country = 'Switzerland'
country_geo_id = '106693272'
file_name = "job_description.txt"


def get_job_description_url_list():
    # building linkedin link
    posit = '%20'.join(postings_name.split())
    url = f'https://www.linkedin.com/jobs/search?keywords={posit}&location={country}&geoId={country_geo_id}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
    
    # it says how many times should thepage be refreshed 
    numb_refresh_page = 0
    
    # opening url in Chrome browser
    print("Creating webdriver ... ")
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 2)
    driver.get(url)
    previous_height = driver.execute_script('return document.body.scrollHeight')

    print("Retrieving job posts URLs ...")
    
    while True:
        # scrolling to the bottom of body height (y coordinate)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        # pausing for 1 sec to load
        time.sleep(1)
        # assigning webpage's increased body height in pixels
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            next_page_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'infinite-scroller__show-more-button')))
            next_page_button.click()
            numb_refresh_page += 1
            if numb_refresh_page == 10:
                break

        # updating previous height for the next loop
        previous_height = new_height
    print("Job posts retrieved.")

    links = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')
    links_list = [link.get_attribute('href') for link in links]

    print("Number of links created " + str(len(links_list)))
    driver.quit()
    return links_list


def scrape_job_description(links_list):
    job_description_list = []
    f = open(file_name, "w+", encoding='utf-8')
    counter = 1
    # looping through the links
    for link in links_list:
        # converting to BeautifulSoup
        request = requests.get(link)
        print(str(counter) + ". " + str(request))
        soup = BeautifulSoup(request.text, 'lxml')
        # extracting text based in class
        try:
            job_description = soup.find('div', class_="show-more-less-html__markup").get_text(separator=" ")
            print(job_description)
            lang = detect(job_description)
            # Translate to English
            if lang != 'en':
                print("Translation incoming from language: " + str(lang))
                translator = Translator()
                print(type(job_description))
                job_description = translator.translate(job_description, src=lang, dest='en').text
        except AttributeError as e:
            print("ERROR! Failed to find the desired element.")
            print("Exception:", type(e).__name__)
            print("Exception details:", str(e))
            traceback.print_exc()
        except Exception as e:
            print("ERROR! In retrieving data...")
            print("Exception:", type(e).__name__)
            print("Exception details:", str(e))
        # # appending to a string and converting to lowercase
        job_description = job_description.replace('\n', ' ')
        job_description_list.append(job_description)
        # # pausing to avoid error 429
        time.sleep(0.6)
        counter += 1
    return job_description_list