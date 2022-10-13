from flask import Flask, render_template, request, redirect, send_file
from extract.indeed import extract_indeed_jobs
from tocsvfile import save_to_file
import jobdb
app = Flask("JobScrapper")


@app.route("/")
def home():
    return render_template("home.html", name="BigDO")


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword is None:
        return redirect("/")
    else:
        data_list = jobdb.load_db(keyword)
        jobs = extract_indeed_jobs(keyword)

        # Check if job in DB already
        for job in jobs:
            found = False
            for data in data_list:
                if job["Company"] == data["company"] and job["Position"] == data["position"] and job["Location"] == data["location"]:
                    found = True
                    break

            if not found:
                job['keyword'] = keyword
                jobdb.insert_record(job)

    return render_template("search.html", keyword=keyword, jobs=jobs)


@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword is None:
        return redirect("/")
#    if keyword not in db:
#        return redirect(f"/search?keyword={keyword}")
#    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")

