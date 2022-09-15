from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


def get_job_keyword():
    key_word = input("Please enter job keyword: ")

    return extract_indeed_jobs(key_word)


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
    results = []
    pages = get_page_count(key_word)
    print("Found", pages)
    for page in range(pages):
        browser = webdriver.Chrome(options=options)
        browser.get(f"https://ca.indeed.com/jobs?q={key_word}&start={page * 10}")
        print(browser)
        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_search = soup.find("ul", class_="jobsearch-ResultsList css-0")
        jobs = job_search.find_all("li", recursive=False)   # Only find 'li' that is directly related to 'ul'

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone is None:
                # h2 = job.find("h2", class_="jobTitle")
                anchor = job.select_one("h2 a")    # Find 'a' inside of h2
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")

                job_data = {
                    "Company": company.string,
                    "Position": title,
                    "Location": location.string,
                    "Link": f"https://ca.indeed.com{link}"
                }
                results.append(job_data)

        for result in results:
            for key, value in result.items():
                print(f"{key}: {value}")
            print("-----------------------------------------------------------------------------------------------------------------")


get_job_keyword()

