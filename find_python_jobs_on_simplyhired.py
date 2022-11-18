"""
This script find all jobs detail in all pages for a job search on simplyhired
website and retrieve all jobs detail. Then it save in a text file named
jabs.txt.
Just using python requests and Beautifulsoup.
"""

import requests
from bs4 import BeautifulSoup


def find_all_jobs_url(url):

    """
    This function retrieve all links page per page and return a list
    with all jobs link.
    url : A Job search url.
    job_links_list : The list returned by this function.
    """

    job_links_list = []
    number_of_page = 1
    res = requests.get(url)
    print(f"retrieving {url}")
    while True:

        soup = BeautifulSoup(res.text, "lxml")
        job_links_list += soup.find_all("a", class_="SerpJob-link card-link")
        nav = soup.find(
            "nav", class_="pagination Pagination Pagination--withTotalJobCounts"
        )
        nex_page = nav.find("a", class_="Pagination-link next-pagination")

        if nex_page:
            url = "https://www.simplyhired.com" + nex_page["href"]
            print(f"retrieving {url}")
            res = requests.get(url)
            number_of_page += 1
        else:
            break
    print(f"Total page retrieved : {number_of_page}")
    print(f"Total job links : {len(job_links_list)}")
    return job_links_list


def find_jobs_detail(urls):
    """
    This function retrieve all detail of all jobs
    urls : Is a list of job link.
    """
    print("retrieving Jobs detatil ...")
    with open("jobs.txt", "w") as jobs:
        for index, url in enumerate(urls):
            url = "https://www.simplyhired.com" + url["href"]
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "lxml")
            job_detail = soup.find("div", class_="p")

            jobs.write("-----------------------------------------------\n")
            jobs.write("-----------------------------------------------\n")
            jobs.write("\n")
            jobs.write(f"Job {index +1} \n")
            jobs.write("\n")
            jobs.write(f"{job_detail.text} \n")
            jobs.write("\n")
    print("Finish - you can find all jobs detail in jobs.txt file")


if __name__ == "__main__":
    url = "https://www.simplyhired.com/search?q=junior+python+developer&fdb=1"
    urls = find_all_jobs_url(url)
    find_jobs_detail(urls)
