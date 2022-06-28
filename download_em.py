
import requests
import csv
import time
import os.path
import sqlite3

filenames = {}

def scrape_with_db():
    connect_with_db = sqlite3.connect('explanatory_memoranda.db')
    cur = connect_with_db.cursor()

    cur.execute("SELECT bill_url, document_link, key FROM explanatory_memoranda WHERE link_type = 'html'")
    links_list = cur.fetchall()
#    print(links_list)

    for row in links_list:
        cur.execute("SELECT bill_name FROM bills WHERE bill_url = ?", (row[0], ))
        bill_name_list = cur.fetchall()

        filename = bill_name_list[0][0] + f"_{row[2]}"

        if os.path.exists('explanatory_memoranda/' + filename):
            continue
        print("Checked:" + filename)

        gotit = False
        while not gotit:
            try:
                page = requests.get(row[1])
                gotit = True

            except:
                print("Failed to download. Trying again")
                time.sleep(5)

        page.encoding = 'utf-8'

        with open('explanatory_memoranda/' + filename, "w") as outputfile:
            outputfile.write(page.text)

    connect_with_db.commit()
    connect_with_db.close()

scrape_with_db()
