from datetime import datetime
from this import d
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
month = date.month
day = date.day

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

for volunteer in volunteers:
    name = volunteer.get("name")
    email = volunteer.get("email")
    to = "To: {}\r\nSubject: {}\r\n\r\n".format(
        email, f"free this {weekday}?"
    )
    message = (
        f"{to}"
        f"Hello {name}! Welcome to the Climate Changemakers community.\n\n"
        f"I'm Matt Stevenson, a Climate Change Makers ambassador, and I'm reaching out "
        f"to see if I can answer any questions you might have. "
        f"I would also like to invite you "
        f"to join me this {weekday} {month}/{day} for an hour of action! "
        f"As we head towards the midterms, "
        f"we would love to have you join and increase our impact. "
        f"Now is the perfect time to really make your action count!\n\n"
        f"Link to the hour of action: https://lu.ma/4ykcvbou \n\n"
        f"Let me know if you have any questions, and hope to see you there!\n\n"
        f"Matt Stevenson\n\n"
        f"https://www.climatechangemakers.org/action-hub"
    )
    print(message)

    s.sendmail(TEST_SEND_EMAIL, [email], message)

# terminating the session
s.quit()
