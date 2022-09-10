import requests
from bs4 import BeautifulSoup


def job_search(key_word):
    results = []
    job_url = f"https://remoteok.com/remote-{key_word}-jobs"

    request = requests.get(job_url, headers={"User-Agent": "My_user_agent"})

    print('-----------------------------------------------------------------------------------------------------------------')
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")
        jobs = soup.find_all('table', id="jobsboard")
        for job_section in jobs:
            job_posts = job_section.find_all('tr', class_="job")
            for post in job_posts:
                link = post['data-href']
                job_info = post.find('td', class_="company position company_and_position")
                job_role = post.find('td', class_="tags")
                name = job_info.find('h3', itemprop="name")
                title = job_info.find('h2', itemprop="title")
                job_tags_list = [job_tag.text for job_tag in job_info.find_all("div", class_='location')]
                job_role_tags = [job_des.text for job_des in job_role.find_all("h3")]

                job_data = {
                    "Company": name.string.strip(),
                    "Title": title.string.strip(),
                    "Job_info (Location, Salary)": (', '.join(map(str, job_tags_list))),
                    "job_tag": (', '.join(map(str.strip, job_role_tags))),
                    "link": f"https://remoteok.com/{link}"
                }

                results.append(job_data)

    else:
        print(f"Can't request {job_url}")

    for job in results:
        for key, value in job.items():
            print(f"{key}: {value}")
        print('-----------------------------------------------------------------------------------------------------------------')
    print(f'{len(results)} jobs are found')


job_search('Python')

