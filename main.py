import csv
import requests
from bs4 import BeautifulSoup


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
    print(str(next_page)) # printing URL for viewing
    response = requests.get(str(next_page)) # getting content wuth requests
    soup = BeautifulSoup(response.content, 'html.parser') # parsing content with BS4

    print(response)
    print(page_num)

    # if page_num < 25:
    #     page_num = page_num + 25
    #     linkedin_scrape(url, 0) # feed page_num var in here, and modify if condition to configure length of

    jobs = soup.find_all('a', class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]")
    for job in jobs:
        job_url = job.get('href')
        # print(job_url)
        response = requests.get(job_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        body = soup.find('div', class_="show-more-less-html__markup").text
        # body = job.find('div', class_="show-more-less-html__markup")
        print(body)

linkedin_scrape(url, 0)