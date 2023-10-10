## ------------------------------------------ ##
## -------- NOT NECESSARY BACKUP------------- ##
## ------------------------------------------ ##
# old -main function it will scrape and save the job descriptions

import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import advertools as adv
import matplotlib.pyplot as plt
from selenium.webdriver.common.by import By
import sys
import re
from langdetect import detect
from googletrans import Translator
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# specifying URL and number of job postings
postings_name = 'Java'
position_num = 100  # numbers 1 to 175 in one page

# building linkedin link
posit = '%20'.join(postings_name.split())
url = f'https://www.linkedin.com/jobs/search?keywords={posit}&location=Switzerland&geoId=106693272&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
f = open("../resources/job_descriptions.txt", "w", encoding='utf-8')

# opening url in Chrome browser
print("Creating webdriver ... ")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('detach', True)
options.add_argument("headless")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver,2)
driver.get(url)
previous_height = driver.execute_script('return document.body.scrollHeight')

print("Retrievin job posts url's ...")
c = 0
while True:
    # scrolling to the bottom of body height (y coordinate)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    # pausing for 1 sec to load
    time.sleep(1)
    # assigning webpage's increased body height in pixels
    new_height = driver.execute_script('return document.body.scrollHeight')
    # breaking the loop once the body stops growing
    if new_height == previous_height:
        next_page_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'infinite-scroller__show-more-button')))
        next_page_button.click()
        print("Button is found")
        c+=1
        if c == 10:
            break
    # updating previous height for the next loop
    previous_height = new_height
print("Job posts retrieved.")

# %% [markdown]
lnks = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')

# looping through classes and extracting hrefs into a list
links_list = []
for lnk in lnks:
    links_list.append(lnk.get_attribute('href'))
print("len: "  + str(len(links_list)))
driver.quit()
print("Link list created.")

# %%
counter = 1
# looping through the links
for link in links_list:
    # converting to BeautifulSoup
    request = requests.get(link)
    print(str(counter) +  ". " + str(request))
    soup = BeautifulSoup(request.text, 'lxml')
    # extracting text based in class
    try:
        job_description = soup.find('div', class_="show-more-less-html__markup").get_text(separator = " ")
        lang = detect(job_description)
        #Translate to English
        if lang != 'en':
            print("Translation incoming from lanuage: " + str(lang))
            translator = Translator()
            job_description = translator.translate(job_description, src=lang, dest='en').text
    except:
        print("ERROR! In retrieving data... ")
    # # appending to a string and converting to lowercase
    job_description = job_description.replace('\n', ' ')
    f.write(job_description.strip())
    f.write("\n\n")
    # # pausing to avoid error 429
    time.sleep(0.6)
    counter+=1


f.close()
