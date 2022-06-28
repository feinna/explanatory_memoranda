import sqlite3
import csv

# CHOOSE DATABASE: old; new

#connect_with_db = sqlite3.connect('../Thesis_python/thesis_mvp.db')
connect_with_db = sqlite3.connect('explanatory_memoranda.db')

#CREATE CURSOR OBJECT
cur = connect_with_db.cursor()

with open('db_extraction_new.csv', 'a', encoding = 'UTF8', newline='') as file:
    writer = csv.writer(file)

    # CHOOSE DATABASE: old one, or new one
    #cur.execute("SELECT key, bill_url, document_link, document_type, link_type FROM em_data")
    cur.execute("SELECT key, bill_url, document_link, document_type, link_type FROM explanatory_memoranda")
    db_extraction = cur.fetchall()

    for row in db_extraction:
        key = row[0]
        bill_url = row[1]
        document_link = row[2]
        document_type = row[3]
        link_type = row[4]

        db_extraction_data = [key, bill_url, document_link, document_type, link_type]
        writer.writerow(db_extraction_data)

connect_with_db.close()
