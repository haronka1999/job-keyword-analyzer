from scrape_methods import get_job_description_url_list,scrape_job_description
import get_keywords 
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import random

"""
Notes:
1. This is the main file this should be called every time
THe other scripts are just helpers which needs to be migrated

    
    getkeywords:  after keywords are retrieved with linkedsent we will apply specific language models to the data    
    preprocess: contains helper functions which needs to be preprocessed before we are apply to the model


    Usage:
    1. First invoke the get_job_description_url_list --> get all of the links job descriptions
    2. Than invoke scrape_job_descriptions: This will scrape from the links the job description part
"""

file_path = "resources/job_descriptions.txt"

## ------------------------------------------ ##
## ------------ FIRST PART ------------------ ##
## ------ EXTRACTING JOB DESCRIPTIONS ------- ##
## ------------------------------------------ ##

# link_list = get_job_description_url_list()
# job_description_list = scrape_job_description(link_list)
# job_description_list = list(set(job_description_list));

# # Open the file in write mode and write each element followed by a newline
# with open(file_path, 'w') as file:
#     for item in job_description_list:
#         file.write(f"{item}\n")
# print(f"The list has been saved to {file_path}. ")
# print(f"The total number of job descriptions: {str(len(job_description_list))}")

## ------------------------------------------ ##
## ------------ SECOND PART ----------------- ##
## ------ EXTRACTING JOB DESCRIPTIONS ------- ##
## ------------------------------------------ ##

with open('job_descriptions.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]
job_description_list = [element for element in lines if element.strip()]
job_description_string =  ' '.join(job_description_list)
preprocessed_JD = get_keywords.preprocess_data(job_description_string)


## ------------------------------------------ ##
## ------------ THIRD PART ------------------ ##
## ------ APPLYING LANGUAGE MODELSS --------- ##
## ------------------------------------------ ##

print("spacy:")
keywords_spacy = get_keywords.get_keywords_by_spacy(preprocessed_JD)

wordcloud = WordCloud(width=800, height=800, background_color='black', 
                      stopwords=nltk.corpus.stopwords.words('english'),
                      min_font_size=10).generate(' '.join(keywords_spacy))


## ------------------------------------------ ##
## ------------ FORTH PART ------------------ ##
## ------ PLOTTING AND IMG CREATING --------- ##
## ------------------------------------------ ##
plt.figure(figsize=(10, 10), facecolor='Black')
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

# assigning file path
p_name = '_'.join('Java'.split())
f_path = f'resources/images/{p_name}-{str(len(lines))}_{random.randint(10000,99999)}.png'
# saving png
plt.savefig(f_path)
# printing the plot
plt.show()