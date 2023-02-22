import csv
import requests
from bs4 import BeautifulSoup
import re

# TODO: scrape jobs from linkedin
# TODO: scrape jobs from indeed


# id="main-content" class="jobs-search__results-list"

# search software engineer seattle, past week, 50 miles

# https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%20Engineer&location=Seattle%2C%20Washington%2C%20United%20States&locationId=&geoId=104116203&sortBy=R&f_TPR=r604800&distance=50&position=1&pageNum=0

# https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%2BEngineer&location=Seattle%2C%2BWashington%2C%2BUnited%2BStates&locationId=&geoId=104116203&sortBy=R&f_TPR=r604800&distance=50&start=150

"""
search?keywords=Software%2BEngineer
&
location=Seattle%2C%2BWashington%2C%2BUnited%2BStates
&
locationId=
&
geoId=104116203
&
sortBy=R
&
f_TPR=r604800
&
distance=50
$
start=0 >>> start is the page more or less, as you scroll it loads 25 more each time.
"""

url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%2BEngineer&location=Seattle%2C%2BWashington%2C%2BUnited%2BStates&locationId=&geoId=104116203&sortBy=R&f_TPR=r604800&distance=50&start="

# response = requests.get(url)

# # print(response)

# soup = BeautifulSoup(response.content,'html.parser')

# job_title = soup.find('h3', class_="base-search-card__title").text
# print(job_title.strip())

# each individual job listing data (the text body) is located within a seperate URL
# that url is under <a> tag with class="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]"


def linkedin_scrape(url, page_num):
    next_page = url + str(page_num) # constructing the URL
    response = requests.get(str(next_page)) # getting content wuth requests
    soup = BeautifulSoup(response.content, 'html.parser') # parsing content with BS4

    # print(response)
    # print(page_num)

    # if page_num < 25:
    #     page_num = page_num + 25
    #     linkedin_scrape(url, 0) # feed page_num var in here, and modify if condition to configure length of
    # refId=D%2BMfFS0RH7Jek0qpZgF5Ww%3D%3D


    jobs = soup.find_all('a', class_="base-card__full-link")
    ref_id_regex_pattern = re.compile(r'refId=([\w%]+)')
    scraped_jobs_set_test_2 = set()

    for job in jobs:
        job_url = job.get('href')
        job_ref_id = ref_id_regex_pattern.search(job_url).group(1) # strips the ref id from the re.match object produced by .search()
        # ref_id_clean = job_ref_id_raw.group(1) # strips the ref id from the re.match object produced by .search()
        print(str(job_ref_id)) # will print the refId to terminal.

        response = requests.get(job_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        if job_ref_id not in scraped_jobs_set_test_2: # if we have not already seen this job, scrape its data.
            body = soup.find('div', class_="show-more-less-html__markup").text # gets the job post body text

            with open('bulk_search_text.txt', 'a') as f:
                f.write('\n')
                f.write(job_ref_id) # writes the job Id to the bulk data file
                f.write('\n' + body + '\n')
                f.write("----------------------------------------------------------------" + '\n') # creates a human readable seperation between job postings

            scraped_jobs_set_test_2.add(job_ref_id) # adds the job refId to the scraped jobs set, after the scrape has been completed
            print(scraped_jobs_set_test_2)
        else:
            continue # if we hit this else, we have already scraped this job, and should proceed to the next in the for loop.


linkedin_scrape(url, 0)