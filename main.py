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
Notes:
1. This is the main file this should be called every time
THe other scripts are just helpers which needs to be migrated

    linkedsent: old -main function it will scrape and save the job descriptions
    getkeywords:  after keywords are retieved with linkedsent we will apply specific language models to the data    
    preprocess: contains helper functions which needs to be preprocessed before we are apply to the model
    
"""
postings_name = 'Java'
country = 'Switzerland'
country_geo_id = '106693272'
file_name = "job_description.txt"


def get_job_description_url_list():
    # building linkedin link
    posit = '%20'.join(postings_name.split())
    url = f'https://www.linkedin.com/jobs/search?keywords={posit}&location={country}&geoId={country_geo_id}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

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
    c = 0
    while True:
        # scrolling to the bottom of body height (y coordinate)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        # pausing for 1 sec to load
        time.sleep(1)
        # assigning webpage's increased body height in pixels
        new_height = driver.execute_script('return document.body.scrollHeight')
        # breaking the loop once the body stops growing
        break
        if new_height == previous_height:
            next_page_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'infinite-scroller__show-more-button')))
            next_page_button.click()
            c += 1
            if c == 1:
                break
        # updating previous height for the next loop
        previous_height = new_height
    print("Job posts retrieved.")

    links = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')
    links_list = []
    for link in links:
        links_list.append(link.get_attribute('href'))
    print("len: " + str(len(links_list)))
    print("Link list created.")
    driver.quit()
    return links_list


def scrape_job_description(links_list):
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
            #  TODO maybe this throws an error when translating
            job_description = soup.find('div', class_="show-more-less-html__markup").get_text(separator=" ")
            print(job_description)
            lang = detect(job_description)
            # Translate to English
            if lang != 'en':
                print(lang)
                print("Translation incoming from language: " + str(lang))
                translator = Translator()
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
        f.write(job_description.strip())
        f.write("\n\n")
        # # pausing to avoid error 429
        time.sleep(0.6)
        counter += 1
    f.close()


link_list = get_job_description_url_list()
scrape_job_description(link_list)
