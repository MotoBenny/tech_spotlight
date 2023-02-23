import csv
import requests
from bs4 import BeautifulSoup
# import re

# DONE: scrape jobs from linkedin
"""
TODO: handle duplicate job postings
TODO: add error handling for 404 errors or other exceptions
TODO: configure scrape to run against all available jobs for a given search, and retain the number of jobs scraped. 
"""


url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%2BEngineer&location=Seattle%2C%2BWashington%2C%2BUnited%2BStates&locationId=&geoId=104116203&sortBy=R&f_TPR=r604800&distance=50&start="


def linkedin_scrape(url, page_num):
    next_page = url + str(page_num)  # constructing the URL
    response = requests.get(str(next_page))  # getting content wuth requests
    # parsing content with BS4
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = soup.find_all('a', class_="base-card__full-link")

    scraped_jobs_list = []

    for listing in jobs:
        job_url = listing.get('href')

        response = requests.get(job_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # if we have not already seen this job, scrape its data.
        if listing not in scraped_jobs_list:
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
            print(scraped_jobs_list)
        else:
            # if we hit this else, we have already scraped this job, and should proceed to the next in the for loop.
            continue


linkedin_scrape(url, 0)


# TODO: scrape jobs from indeed
