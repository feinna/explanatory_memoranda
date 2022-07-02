# A script to assess readability, count jargon, and count oxford3000 appearances.

from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from readability import Readability
import nltk
import sqlite3
import re
import copy
import os

#SQLITE DATABASE CONNECT
connect_with_db = sqlite3.connect('explanatory_memoranda.db')

#CREATE CURSOR OBJECT
cur = connect_with_db.cursor()

get_em_data = cur.execute("SELECT key, text_no_tables, text_no_digit_tables, cleaned_text FROM explanatory_memoranda WHERE link_type = 'html'")
em_data_list = cur.fetchall()

for row in em_data_list:
    em_key = row[0]
    text_no_tables = row[1]
    text_no_digit_tables = row[2]
    cleaned_text = row[3]

    print(em_key)

    cleaned_readability = Readability(cleaned_text)
    no_tables_readability = Readability(text_no_tables)
    text_no_digits_readability = Readability(text_no_digit_tables)


    try:
        fk_cleaned = cleaned_readability.flesch_kincaid()
        fk_score_cleaned = fk_cleaned.score
        fk_grade_cleaned = fk_cleaned.grade_level

        fk_no_tables = no_tables_readability.flesch_kincaid()
        fk_score_no_tables = fk_no_tables.score
        fk_grade_no_tables = fk_no_tables.grade_level

        fk_no_digits = text_no_digits_readability.flesch_kincaid()
        fk_score_noDigitTables = fk_no_digits.score
        fk_grade_noDigitTables = fk_no_digits.grade_level

        smog_cleaned = cleaned_readability.smog(all_sentences=True)
        SMOG_score_cleaned = smog_cleaned.score
        SMOG_grade_cleaned = smog_cleaned.grade_level

        smog_no_tables = no_tables_readability.smog(all_sentences=True)
        SMOG_score_no_tables = smog_no_tables.score
        SMOG_grade_no_tables = smog_no_tables.grade_level

        smog_no_digits = text_no_digits_readability.smog(all_sentences=True)
        SMOG_score_noDigitTables = smog_no_digits.score
        SMOG_grade_noDigitTables = smog_no_digits.grade_level
    except:
        fk_score_cleaned = "NA"
        fk_grade_cleaned = "NA"

        fk_score_no_tables = "NA"
        fk_grade_no_tables = "NA"

        fk_score_noDigitTables = "NA"
        fk_grade_noDigitTables = "NA"

        SMOG_score_cleaned = "NA"
        SMOG_grade_cleaned = "NA"

        SMOG_score_no_tables = "NA"
        SMOG_grade_no_tables = "NA"

        SMOG_score_noDigitTables = "NA"
        SMOG_grade_noDigitTables = "NA"

    insert_into_readability = cur.execute("INSERT INTO readability (em_key, FK_score_cleaned, FK_grade_cleaned, SMOG_score_cleaned, SMOG_grade_cleaned, FK_score_noTables, FK_grade_noTables, SMOG_score_noTables, SMOG_grade_noTables, FK_score_noDigitTables, FK_grade_noDigitTables, SMOG_score_noDigitTables, SMOG_grade_noDigitTables) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (em_key, fk_score_cleaned, fk_grade_cleaned, SMOG_score_cleaned, SMOG_grade_cleaned, fk_score_no_tables, fk_grade_no_tables, SMOG_score_no_tables, SMOG_grade_no_tables, fk_score_noDigitTables, fk_grade_noDigitTables, SMOG_score_noDigitTables, SMOG_grade_noDigitTables))


    connect_with_db.commit()

#close the connection to the database
connect_with_db.close()
