from datetime import datetime
from dotenv import load_dotenv
import smtplib
import os
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("month", type=int)
parser.add_argument("day", type=int)
parser.add_argument("year", type=int)
args = parser.parse_args()

load_dotenv()
PASSWORD = os.environ.get("PASSSWORD")
TEST_SEND_EMAIL = os.environ.get("TEST_SEND_EMAIL")
TEST_RECEIVE_EMAIL = os.environ.get("TEST_RECEIVE_EMAIL")

volunteers = []
date = datetime(args.year, args.month, args.day)
weekday = date.strftime("%A")

# creates SMTP session
s = smtplib.SMTP("smtp.gmail.com", 587)

# start TLS for security
s.starttls()

# Authentication
s.login(TEST_SEND_EMAIL, PASSWORD)

with open("ccm.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        name = row[1]
        first_name = name.split()[0]
        volunteers.append({"name": first_name, "email": row[0]})
        line_count += 1

    print(f"Processed {line_count} lines.")

for volunteer in volunteers[:1]:
    to = "To: {}\r\nSubject: {}\r\n\r\n".format(
        "matstev2@pdx.edu", f"free this {weekday}?"
    )
    name = volunteer.get("name")
    email = volunteer.get("email")
    message = (
        f"{to}"
        f"Hello {name}! \n\n"
        f"I'm Matt Stevenson, a Climate Change Makers ambassador, and I'm reaching out "
        f"to see if you would like to join me for an hour of action on this coming {weekday}, "
        f"{date.month}/{date.day}.\n\n"
        f"Hope to see you there!\n\n"
        f"Matt Stevenson"
    )
    print(message)

    s.sendmail(TEST_SEND_EMAIL, [TEST_RECEIVE_EMAIL], message)

# terminating the session
s.quit()
