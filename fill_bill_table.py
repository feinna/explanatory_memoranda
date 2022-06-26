from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
import sqlite3
import re
import copy
import os
import csv

#SQLITE DATABASE CONNECT
connect_with_db = sqlite3.connect('explanatory_memoranda.db')

#CREATE CURSOR OBJECT
cur = connect_with_db.cursor()
# look in this folder for files to loop through
data_files = os.listdir("bills")

def fill_bills_table():
    key_number = 0
    for filename in sorted(data_files):
        if filename == ".DS_Store":
            continue

        with open(f"bills/{filename}") as fp:
            soup = BeautifulSoup(fp, features="html5lib")

        print(f"Processing: {filename}")

        # open the csv file and write to it
        key_number = key_number + 1
        bill_name = filename
        html_bill_information = soup.find("dl", {"class": "dl--inline--bills"})
        html_bill_information_list = []

        for child in html_bill_information.children:
            html_bill_information_list.append(child.string)
        try:
            find_portfolio = soup.find("div", {"id": "main_0_billSummary_portfolioPanel"}).dd
            portfolio = find_portfolio.string.strip()
        except:
            portfolio = "NA"

        try:
            find_gov_or_member = html_bill_information.find(string=re.compile("type", re.I))
            gov_or_member = find_gov_or_member.next_element.next_element.string.strip()
        except:
            gov_or_member = "MANUAL"
            with open("exceptions_bills.txt", "a") as file:
                file.write(f"GOV_OR_MEMBER: {changed_title}\n")

        try:
            find_originating_house = html_bill_information.find(string=re.compile("originating house", re.I))
            originating_house = find_originating_house.next_element.next_element.string.strip()
        except:
            originating_house = "MANUAL"
            with open("exceptions_bills.txt", "a") as file:
                file.write(f"ORIGINATING_HOUSE: {changed_title}\n")

        try:
            find_status_of_bill = html_bill_information.find(string=re.compile("status", re.I))
            status_of_bill = find_status_of_bill.next_element.next_element.string.strip()
        except:
            status_of_bill = "MANUAL"
            with open("exceptions_bills.txt", "a") as file:
                file.write(f"STATUS_OF_BILL: {changed_title}\n")

        try:
            find_parliament_number = html_bill_information.find(string=re.compile("parliament no", re.I))
            parliament_number = find_parliament_number.next_element.next_element.string.strip()
        except:
            parliament_number = "MANUAL"
            with open("exceptions_bills.txt", "a") as file:
                file.write(f"PARLIAMENT_NUMBER: {changed_title}\n")

        find_permalink = soup.find("a", {"id": "main_0_billSummary_permalink"})
        permalink = find_permalink.get('href')

        # find the progress section, which houses the dates for introduction of bills to each house, and the assent date
        progress_section = soup.find("div", {"id": "main_0_mainDiv"})
        progress_section_list = []

        #iterate through this section, strip the strings, append to a list that you can run through
        for string in progress_section.stripped_strings:
            progress_section_list.append(string)

        # find the search term 'introduced', which appears twice in this section - once for the house and once for the senate
        reg_in_house = re.compile("introduced.*", re.I)
        find_introduction = [i for i, item in enumerate(progress_section_list) if re.search('Introduced.*', item)]

        # the first value is assigned to originating house, the second to checking house
        introduced_originating_house = progress_section_list[int(find_introduction[0]) + 1]
        introduced_checking_house = progress_section_list[int(find_introduction[1]) + 1]
        assented_date = progress_section_list[len(progress_section_list) - 1]

        #if statement to determine whether originating house was reps, if so then it assigns the originating house data to the representatives variable, and checking to senate variable
        if "Representatives" in originating_house:
            introduced_representatives_date = introduced_originating_house
            introduced_senate_date = introduced_checking_house

        # if originating house was not reps, then it assigns originating house data to the senate variable, and checking to the reps variable
        elif "Senate" in originating_house:
            introduced_senate_date = introduced_originating_house
            introduced_representatives_date = introduced_checking_house

        else:
            introduced_representatives_date = "MANUAL"
            introduced_senate_date = "MANUAL"

        cur.execute("INSERT INTO bills(bill_name, bill_url, gov_or_member, originating_house, portfolio, status_of_bill, parliament_number, date_intro_house, date_intro_senate, date_assented) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (bill_name, permalink, gov_or_member, originating_house, portfolio, status_of_bill, parliament_number, introduced_representatives_date, introduced_senate_date, assented_date))

        connect_with_db.commit()

fill_bills_table()
