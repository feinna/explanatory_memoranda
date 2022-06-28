import sqlite3

connect_with_db = sqlite3.connect('explanatory_memoranda.db')

cur = connect_with_db.cursor()

cur.execute('''CREATE TABLE "bills" ("key" INTEGER UNIQUE, "bill_name" TEXT, "bill_url" TEXT UNIQUE, "gov_or_member" TEXT, "originating_house" TEXT, "portfolio" TEXT, "status_of_bill" TEXT, "parliament_number" INTEGER, "date_intro_house" TEXT, "date_intro_senate" TEXT, "date_assented" TEXT, PRIMARY KEY("key" AUTOINCREMENT))''')
cur.execute('''CREATE TABLE explanatory_memoranda ("key" INTEGER UNIQUE, "bill_url" INTEGER, "document_type" text, "document_link" TEXT, "link_type" TEXT, "unparsed" text, "parsed" text, "cleaned_text" TEXT, "circulated_by" TEXT, "text_no_tables" text, "text_no_digit_tables" text, PRIMARY KEY("key" AUTOINCREMENT), FOREIGN KEY("bill_url") REFERENCES "bills"("bill_url"))''')
cur.execute('''CREATE TABLE readability ("key" INTEGER UNIQUE, "em_key" INTEGER, "FK_score_cleaned" INTEGER, "FK_grade_cleaned" INTEGER, "SMOG_score_cleaned" INTEGER, "SMOG_grade_cleaned" INTEGER, "Oxford3000_count_cleaned" INTEGER, "Jargon_count_cleaned" INTEGER, "word_count_cleaned" INTEGER, "FK_score_noTables" TEXT, "FK_grade_noTables" INTEGER, "SMOG_score_noTables" INTEGER, "SMOG_grade_noTables" INTEGER, "FK_score_noDigitTables" INTEGER, "FK_grade_noDigitTables" INTEGER, "SMOG_score_noDigitTables" INTEGER, "SMOG_grade_noDigitTables" INTEGER, PRIMARY KEY("key" AUTOINCREMENT))''')

connect_with_db.commit()

connect_with_db.close()
