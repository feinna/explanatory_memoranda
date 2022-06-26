#download the bills from the bill information pages using the bill_link.csv file for the urls

import requests
import csv
import time
import os.path

filenames = {}

def scrape_with_csv():
    with open('bill_link.csv') as csvfile:
        spamreader = csv.reader(csvfile)

        firstrow = True
        rowsDone = 0
        for row in spamreader:
            if firstrow:
                firstrow = False
                continue

            # if there are multiple bills with the same name, this provides a unique name by adding a number
            count = filenames.get(row[0], 0)
            filenames[row[0]] = count + 1

            fn = row[0]
            if (count > 0):
                fn = f"{row[0]}_{count}"

            # if script stops for any reason, will check where we're at and start again
            if os.path.exists('bills/' + fn):
                continue

            print("Downloading: " + fn)

            # deals with server timing out or kicking us off
            gotit = False
            while not gotit:
                try:
                    page = requests.get(row[1])
                    gotit = True
                except:
                    print("Download failed. Trying again.")
                    time.sleep(10)

            page.encoding = 'utf-8'

            with open('bills/' + fn, "w") as outputfile:
                outputfile.write(page.text)

scrape_with_csv()
