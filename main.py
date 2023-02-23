import csv
import requests
from bs4 import BeautifulSoup
import os
import re

# import re

# DONE: scrape jobs from linkedin
"""
TODO: handle duplicate job postings
TODO: add error handling for 404 errors or other exceptions
TODO: explore rate limits, for scraper
TODO: optimize for the given rate limits
TODO: configure scrape to run against all available jobs for a given search, and retain the number of jobs scraped.
TODO: perform term search and export to CSV file
"""


url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%2BEngineer&location=Seattle%2C%2BWashington%2C%2BUnited%2BStates&locationId=&geoId=104116203&sortBy=R&f_TPR=r604800&distance=50&start=" #0 or 25 


def linkedin_scrape(url, page_num):
    next_page = url + str(page_num)  # constructing the URL
    response = requests.get(str(next_page))  # getting content wuth requests
    # parsing content with BS4d
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = soup.find_all('a', class_="base-card__full-link")

    scraped_jobs_list = []

    for listing in jobs:
        job_url = listing.get('href')

        response = requests.get(job_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # if we have not already seen this job, scrape its data.
        if job_url not in scraped_jobs_list:
            # gets the job post body text
            body = soup.find('div', class_="show-more-less-html__markup").text

            with open('bulk_search_text.txt', 'a') as f:
                f.write('\n')
                f.write(str(job_url))  # writes the job URL
                f.write('\n' + body + '\n')
                # creates a human readable seperation between job postings
                f.write(
                    "----------------------------------------------------------------" + '\n')

            # adds the job_url to the scraped jobs list, after the scrape has been completed
            scraped_jobs_list.append(job_url)
            print(job_url)
        else:
            # if we hit this else, we have already scraped this job, and should proceed to the next in the for loop.
            continue

# uncomment the line below and run it to perform a initial scrape and create a raw text file of job information.
# linkedin_scrape(url, 0) 


# TODO: scrape jobs from indeed

"""
TODO: create list of regex patterns
TODO: import patterns as list
TODO: search through bulk text data, for each regex pattern /gmi global multiline insensitive search
TODO: save results as dictionary key value pairs
TODO: output the results to a Json Key value object 
"""
#importing file-todo: import file!
def regex_terms(regex_file):
    """_summary_
    Args:
        regex_file (.txt): .txt file containing tech terms, and matching regex patterns
    Returns:
        Dict: a dictionary of key value pairs where key is the term and value is the regex pattern

    NOTE: I believe that this is working as intended and the issue is limited to printing the regex patterns. 

    In this case, we must procced with the application (beginning with the find_tech_occurances function) until we output something that shows us if the regex patterns are working.
    """
    with open(regex_file, "r") as f:
        regex_list = f.readlines()
        # Laravel: \bLaravel\b {'Laravel': '\bLaravel\b', 'PHP': '\bPHP\b'}
    patterns_dict = {}
    for term in regex_list:
        try:
            key, value = term.strip().split(": ")
            patterns_dict[key] = value

        except ValueError:
            continue

    return patterns_dict

path = 'patterns.txt'
regex_dict = regex_terms(path)
print(regex_dict)


# from patterns import patterns_dict
# print(patterns_dict)

def find_tech_occurrences(text_file, patterns_dict):
    """
    TODO: open the raw text file
    TODO: for each value in patterns_dict, search through the raw text
    TODO: incriment a new results dict, where key = key from patterns_dict, and value = number of times that term was found in raw text
    TODO: return results dict
    """
    pass

def results_to_json(results_dict):
    """
    TODO: convert results_dict to json
    """
    pass

def upload_results_to_db(results_json):
    """
    TODO: sort out all the DB stuff.....
    """
    pass

"""
steps
* open the bulk_search_text file
* import pattern.txt as a list of regex patterns
* import regex--DONE
* search the bulk data for each regex pattern
* save results as dictionary key value pairs where key us the tech term, and value is how many times it was found in bulk text
* convert that dictionary to .JSON format

"""

