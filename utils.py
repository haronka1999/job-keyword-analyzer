import unicodedata
import preprocess   

"""
Here comes evert utility function
"""

def read_jobs():
    with open('../resources/job_descriptions.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    # Remove newline characters from each line
    lines = [line.strip() for line in lines]
    job_descriptions = [element for element in lines if element.strip()]
    return ' '.join(job_descriptions)



def preprocess_data(jobs):
    # MANDATORY PREPROCESS:

    # remove accented characters
    jobs = unicodedata.normalize('NFKD', jobs).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    jobs = preprocess.expand_contractions(jobs)
    jobs = preprocess.remove_special_characters(jobs)
    jobs = preprocess.remove_punctuation(jobs)
    jobs = preprocess.remove_extra_whitespace_tabs(jobs)
    jobs = preprocess.remove_punctuation(jobs)

    # jobs = preprocess.get_stem(jobs)
    # jobs = preprocess.replace_numbers(jobs)
    # jobs = preprocess.remove_months(jobs)
    # jobs = preprocess.remove_numbers(jobs)
    
    f = open("resources/preprocessed_text.txt", "w", encoding='utf-8')
    f.write(jobs)
    f.close()
    return jobs