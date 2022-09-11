import requests
from bs4 import BeautifulSoup


# Get a job keyword from the user
def get_job_keyword():
    job_keyword = input("Please enter job keyword: ")

    return search_job(job_keyword)


# Search a job keyword
def search_job(keyword):
    job_result = []

    job_url = f"https://remoteok.com/remote-{keyword}-jobs"
    request = requests.get(job_url, headers={"User-Agent": "My_user_agent"})
    print('-----------------------------------------------------------------------------------------------------------------')
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs_board = soup.find_all("table", id="jobsboard")
        for job in jobs_board:
            job_posts = job.find_all("tr", class_="job")
            for post in job_posts:
                job_links = post["data-href"]
                job_info = post.find("td", class_="company position company_and_position")
                job_role = post.find("td", class_="tags")
                company_name = job_info.find("h3", itemprop="name")
                job_title = job_info.find("h2", itemprop="title")
                job_info_tags = [info_tag.text for info_tag in job_info.find_all("div", class_="location")]
                job_role_tags = [role_tag.text for role_tag in job_role.find_all("h3")]

                job_data = {
                    "Company": company_name.string.strip(),
                    "Title": job_title.string.strip(),
                    "Job_info (Location, Salary)": (", ".join(map(str, job_info_tags))),
                    "Job_role": (", ".join(map(str.strip, job_role_tags))),
                    "Link": f"https://remoteok.com/{job_links}"
                }

                job_result.append(job_data)
    else:
        print(f"Can't request {job_url}. Please enter again.")
        get_job_keyword()

    for job in job_result:
        for key, value in job.items():
            print(f"{key}: {value}")
        print('-----------------------------------------------------------------------------------------------------------------')
    print(f'{len(job_result)} jobs are found')


get_job_keyword()
