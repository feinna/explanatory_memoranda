# explanatory_memoranda

*2 July 2022*


Hello! This is a project to download the html of Australian federal government explanatory memoranda and have them all available in a database, rather than individual documents sitting on the web.

If you've arrived via my thesis, please note the following changes:
1. aph_scraper.py is now several documents. You'll want to look at build_bill_link_csv.py, fill_bill_table.py, and build_em_link_dbtable.py
2. scraper.py is now several documents. You'll want to look at download_bills.py and download_em.py
3. mvp.py is still one file, but it's now called process_em_text.py
4. readability_script.py is the same file, same name.


**DATABASE FILES**


So, I have not put the database anywhere on the internet, but these files will help you build your own. Please note that you will need to do a manual search of the APH website, and save each search html page (making sure to change the # of results per page to 100).
Please read each of the files in advance so that you know which folders things should be on in your project foleder, and the locations where you can change the names of files.
You will need to use sqlite3 for the database. I use DB browser for sqlite to look at my database, and you can too (links below).


**RUN ORDER**
1. construct_database.py will build the database frame for you to slot the data into
2. build_bill_link_csv.py will build you a csv file so that you can download the bill html information pages
3. download_bills.py will download each bill in your search results
4. fill_bill_table.py will parse the bill html files and input into your database. Please make sure that you have a closed database before you do this.
5. build_em_link_dbtable.py will parse the bill html files for the explanatory memoranda document links and input into the explanatory_memoranda table in db.
6. download_em.py will download your explanatory memoranda html docs.
7. process_em_text will parse those em files, match against the document_link via permalink, and update the explanatory_memoranda table in db. Again: closed db only.
8. readability_script.py will update the readability table with readability stats. It uses the py readability library (see link below)


**PYTHON LIBRARIES USED**


Requests: https://pypi.org/project/requests/


BeautifulSoup4: https://pypi.org/project/beautifulsoup4/


Sqlite3: https://docs.python.org/3/library/sqlite3.html


Py-readbility-metrics: https://pypi.org/project/py-readability-metrics


os, csv, copy, re



**PROGRAMS I ALSO USED THAT YOU MAY ALSO LIKE**


DB Browser for SQLite: https://sqlitebrowser.org/


Atom text editor: https://atom.io/
