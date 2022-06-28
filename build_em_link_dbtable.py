# scrapes each bill file for the section listing the explanatory memoranda, then pulls the link for the pdf, word, and html files and puts them into the explanatory_memoranda table of the database with the associated bill name and type of link (word, pdf, html) and the type of explanatory memoranda (EM, supplementary, revised, etc)

from bs4 import BeautifulSoup
import requests
import csv
import os
import sqlite3

connect_with_db = sqlite3.connect('explanatory_memoranda.db')

#CREATE CURSOR OBJECT
cur = connect_with_db.cursor()

data_files = os.listdir("bills")

def scrape_bill_for_em_link():

    #open each bills file, and insert a row for each link with a key, permalink (as fk),and document type

    key_number = 0
    for filename in sorted(data_files):
        if filename == ".DS_Store":
            continue
        #inform which file working on

        #open the file and make a soup object
        with open(f"bills/{filename}") as fp:
            soup = BeautifulSoup(fp, features="html5lib")

        key_number = key_number + 1

        find_permalink = soup.find("a", {"id": "main_0_billSummary_permalink"})
        permalink = find_permalink.get('href')

        html_docs_list = []

        print("Working on:" + filename)


        # section to deal with the explanatory memoranda html document
        em_number = 0

        #this may be arbitrary numbering
        while em_number < 10:
            em_docs_urls = {}
            find_em_docs = soup.find("tr", {"id":f"main_0_explanatoryMemorandaControl_readingItemRepeater_trFirstReading1_{em_number}"})
            if find_em_docs == None:
                html_docs_list.append("NULL")
                break
            find_em_type = find_em_docs.find("ul", {"class" : "links"})
            em_type = find_em_type.string


            for link in find_em_docs.find_all('a'):
                getlink = link.get('href')
                em_docs_urls[getlink] = em_type

            for x,y in em_docs_urls.items():

                if "pdf" in x:
                    cur.execute("INSERT INTO explanatory_memoranda(bill_url, document_link, link_type, document_type) VALUES (?, ?, ?, ?);", (permalink, x, "pdf", y))
                    connect_with_db.commit()

                elif "word" in x:
                    cur.execute("INSERT INTO explanatory_memoranda(bill_url, document_link, link_type, document_type) VALUES (?, ?, ?, ?);", (permalink, x, "msword", y))
                    connect_with_db.commit()
                else:
                    cur.execute("INSERT INTO explanatory_memoranda(bill_url, document_link, link_type, document_type) VALUES (?, ?, ?, ?);", (permalink, x, "html", y))
                    connect_with_db.commit()

            em_number = em_number + 1

        connect_with_db.commit()


scrape_bill_for_em_link()

connect_with_db.close()
