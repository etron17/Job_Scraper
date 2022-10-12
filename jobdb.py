from dotenv import load_dotenv
import mysql.connector
import os
from file import save_to_file
from extract.indeed import extract_indeed_jobs

load_dotenv()
# Environment variables

mydb = mysql.connector.connect(
    host=os.getenv("your_host"),
    user=os.getenv("your_user"),
    password=os.getenv("your_password"),
    database=os.getenv("your_database")
)

print(mydb)

mycursor = mydb.cursor(dictionary=True)

# Create DB
#mycursor.execute("DROP TABLE IF EXISTS Jobs")
#mycursor.execute("CREATE TABLE Jobs (job_id SERIAL PRIMARY KEY, keyword VARCHAR(100), "
#                 "company VARCHAR(200), position VARCHAR(200), location "
#                 "VARCHAR(200), link VARCHAR(2000))")
#mycursor.execute("INSERT INTO Jobs (keyword, company, position, location, link) VALUES ('python', 'ABC', 'Position 1', 'Location 1', 'Link1'")


def load_db(keyword: str):
    mycursor.execute('''SELECT * from Jobs WHERE keyword=\'%s\'''' % (keyword))
    data = mycursor.fetchall()
    return data


def convert_str(value: str):
    if value is None:
        return "NULL"
    else:
        return "{}".format(value)

def insert_record(data: dict):
    sql = "INSERT INTO Jobs (keyword, company, position, location, link) VALUES (%s, %s, %s, %s, %s)"
    values = (convert_str(data["keyword"]), convert_str(data["Company"]), convert_str(data["Position"]), convert_str(data["Location"]), convert_str(data["Link"]))
    mycursor.execute(sql, values)
    mydb.commit()
