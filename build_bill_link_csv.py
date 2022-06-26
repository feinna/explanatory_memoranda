# Pulls the title and url for the bill html from a list of search results in the manually downloaded files

from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
import os
import csv

def build_bill_link_csv():
    key_number = "1"
    filename = key_number + ".html"
    data_files = os.listdir("search_results")

    for filename in data_files:
        if filename == ".DS_Store":
            continue

        print(f"Working on: {filename}")

        with open(f"search_results/{filename}") as fp:
            soup = BeautifulSoup(fp, features="html5lib")

        bill_number = 0
        with open('bill_link.csv', 'a', encoding = 'UTF8', newline='') as file:
            writer = csv.writer(file)

            while bill_number < 100:
                bill_name_tags = soup.find("a", {"id":f"main_0_content_0_lvResults_hlTitle_{bill_number}"})
                if bill_name_tags == None:
                    break
                bill_url_get = bill_name_tags.get('href')
                make_it_nice = "https://www.aph.gov.au" + bill_url_get
                bill_data = [bill_name_tags.string, make_it_nice]
                writer.writerow(bill_data)
                bill_number = bill_number + 1

build_bill_link_csv()
