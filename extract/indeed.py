from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()


def get_job_keyword():
    key_word = input("Please enter job keyword: ")

    return extract_indeed_jobs(key_word)


# The maximum number of pages are limited by 5. -> Prevent massive requests
def get_page_count(key_word):
    browser = webdriver.Chrome(options=options)
    browser.get(f"https://ca.indeed.com/jobs?q={key_word}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", role="navigation")
    if pagination is None:
        return 1

    pages = pagination.find_all("div", recursive=False)
    count = len(pages)

    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(key_word):
    results = []    # Store jobs
    pages = get_page_count(key_word)
    print("Found", pages)
    for page in range(pages):
        browser = webdriver.Chrome(options=options)
        browser.get(f"https://ca.indeed.com/jobs?q={key_word}&start={page * 10}")
        print(browser)
        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_search = soup.find("ul", class_="jobsearch-ResultsList css-0")
        jobs = job_search.find_all("li", recursive=False)   # Only find 'li' that is directly related to 'ul'

        # Enter into li
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone is None:
                anchor = job.select_one("h2 a")    # Find 'a' inside of h2
                title = anchor['aria-label']    # Find 'aria-label'
                link = anchor['href']   # Find 'href'
                company = job.find("span", class_="companyName")    # Find 'span' that class name is 'companyName'
                location = job.find("div", class_="companyLocation")   # Find 'div' that class name is 'companyLocation'

                # Store company's info into dictionary{key:value}
                job_data = {
                    "Company": company.string,
                    "Position": title,
                    "Location": location.string,
                    "Link": f"https://ca.indeed.com{link}"
                }
                results.append(job_data)
        # Print out each element from dictionary
        for result in results:
            for key, value in result.items():
                print(f"{key}: {value}")
            print("-----------------------------------------------------------------------------------------------------------------")


get_job_keyword()

