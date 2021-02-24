import requests
import time
import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
c = db()
conn = c

email_list = []

TESTMAIL_API_KEY = os.getenv("TESTMAIL_API_KEY")

def current_milli_time():
    return round(time.time() * 1000)

def get_email():
    s = requests.Session()
    s.max_redirects = float("inf")

    while True:
        t = current_milli_time()
        emails = s.get(f"https://api.testmail.app/api/json?apikey={TESTMAIL_API_KEY}&namespace=5v6g6&tag=forwardemail&timestamp_from={t}&livequery=true")

        print(emails)


        if [str(emails.json()["emails"][0]["timestamp"]), emails.json()["emails"][0]["subject"], emails.json()["emails"][0]["to"], emails.json()["emails"][0]["from"]] not in email_list:
            email_list.append([str(emails.json()["emails"][0]["timestamp"]), emails.json()["emails"][0]["subject"], emails.json()["emails"][0]["to"], emails.json()["emails"][0]["from"]])
            print(str(emails.json()["emails"][0]["timestamp"]), emails.json()["emails"][0]["subject"], emails.json()["emails"][0]["to"], emails.json()["emails"][0]["from"])


            c.execute("INSERT INTO dashboard_email (timestamp, subject, body, from_email, to_email) VALUES (:timestamp, :subject, :body, :from_email, :to_email)", {
                "timestamp": str(emails.json()["emails"][0]["timestamp"]),
                "subject": emails.json()["emails"][0]["subject"],
                "body": emails.json()["emails"][0]["html"],
                "from_email": emails.json()["emails"][0]["from"],
                "to_email": emails.json()["emails"][0]["to"]
            })
            conn.commit()


        time.sleep(0.001)


get_email()