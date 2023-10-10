from scrape_methods import get_job_description_url_list,scrape_job_description
from get_keywords import get_keywords_by_spacy

"""
Notes:
1. This is the main file this should be called every time
THe other scripts are just helpers which needs to be migrated

    linkedsent: old -main function it will scrape and save the job descriptions
    getkeywords:  after keywords are retrieved with linkedsent we will apply specific language models to the data    
    preprocess: contains helper functions which needs to be preprocessed before we are apply to the model


    Usage:
    1. First invoke the get_job_description_url_list --> get all of the links job descriptions
    2. Than invoke scrape_job_descriptions: This will scrape from the links the job description part
"""


## ------------------------------------------ ##
## ------------ FIRST PART ------------------ ##
## ------ EXTRACTING JOB DESCRIPTIONS ------- ##
## ------------------------------------------ ##

# link_list = get_job_description_url_list()
# job_description_list = scrape_job_description(link_list)
# job_description_list = list(set(job_description_list));
# file_path = "job_descriptions.txt"
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


