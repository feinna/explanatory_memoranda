# A script to parse the scraped HTML of federal government explanatory memoranda,
#including unparsed and parsed text, document type, title of dopcument,
#text with no tables, and text with tables that meet a set criteria regarding number of digits

from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
import sqlite3
import re
import copy
import os

#SQLITE DATABASE CONNECT
connect_with_db = sqlite3.connect('explanatory_memoranda.db')
cur = connect_with_db.cursor()

# This is a function to check whether a cell is mostly numbers or mostly letters, to determine whether it should be removed or retained from text_no_tables
# This is so we can keep tables that have been selected for formatting purposes, rather than because they are tables
# Readability formulas work for word text, but don't perform well with digits, so we want to remove them while keeping the text that is mostly words.
# Thesis did not end up using text_no_digit_tables, instead looking only at cleaned_text and text_no_tables.

def are_you_mostly_numbers(table_cell):
    table_cell_text = table_cell.get_text()
    character_count = len(table_cell_text)
    numbers_count = len(re.findall("\d", table_cell_text))

    # This is arbitrary - I simply decided that 20% was a good number; another reason not to use until there is a more solid justification
    boundary_value = character_count / 5

    if numbers_count >= boundary_value and numbers_count >= 1:
        return True
    else:
        return False

# This function removes the string "Parlinfo -" from the start of the title text, which is present in all titles
def remove_parlinfo_from_title(title_string):
    change_string = re.sub("ParlInfo - ", "", title_string, re.I)
    return change_string

# Clean the table data by removing additional spaces, new lines, and carriage returns so that it's readable. This is to smooth over the text in preparation for readability stats, which might
# consider a new line or carriage return to mean that the text is a heading, and therefore the end of a sentence.

def clean_table_data(text_from_soup):
    text_rem_spaces = re.sub('\s{2,}', ' ', text_from_soup)
    text_rem_newlines = re.sub('\\n+', ' ', text_rem_spaces)
    text_rem_carriagereturns = re.sub('\\r+', ' ', text_rem_newlines)
    clean_table_data = text_rem_carriagereturns
    return clean_table_data

# Function removes the tables from the text (where tables have the tag 'table'), either in full (all) or just the ones where a boundary value for the acceptable number of digits has been breached
def removing_tables(removal_type):
    new_soup = copy.copy(soup)
    find_the_tables = new_soup.find_all('table')

    # If "digits" is passed in, then remove the tables that exceed the boundary and numbers conditiions in the are_you_mostly_numbers function above.
    if removal_type == "digits":
        for x in find_the_tables:
            find_the_row = x.find_all('td')
            more_numbers_than_letters = 0

            # loop through the cells in a table, sending back True/False based on whether they are mostly digits/whitespace
            for table_cell in find_the_row:
                if are_you_mostly_numbers(table_cell) == True:
                    more_numbers_than_letters = more_numbers_than_letters + 1

            # determine if the number of True/False is enough to remove the whole table; if statement for remove or retain in table
            # this, again, is an arbitrary decision of 10%
            table_boundary_for_removal = len(find_the_row) / 10

            # update the doublesoup object as above
            if more_numbers_than_letters >= table_boundary_for_removal:
                x.decompose()
        return new_soup

    elif removal_type == "all":
        for x in find_the_tables:
            x.decompose()
        return new_soup

    else:
        print("Tables could not be removed. Please check whether you've specified digits only (digits) or all table values (all)")

# finds the first instance of a four digit text after the function is called (which is at <div class = "box") and then removes the three hyperlinks that follow.
# this is to remove the 'bill home', 'download word' and 'download pdf' sections that sit between the bill title and the year information which is part of
# the html pages, but not part of the document itself

def remove_this_text(which_soup_text):
    safetytext = copy.copy(which_soup_text)
    find_first = which_soup_text.find(string=re.compile("\d{4}", re.I))

    safetytext.a.decompose()
    safetytext.a.decompose()
    safetytext.a.decompose()

    return safetytext.get_text()

# Loop through files in directory where EMs have been downloaded
data_files = os.listdir("explanatory_memoranda")
key_number = 0

for filename in data_files:
    if filename == ".DS_Store":
        continue

    # open each file
    with open(f"explanatory_memoranda/{filename}") as fp:
        soup = BeautifulSoup(fp, features="html5lib")

    # tell the console what you're doing so we're not just left in the dark
    print(f"Processing: {filename}")

    # Find the permalink so that you can match it against the database document_link
    find_permalink = soup.find("a", {"class": "permalink"})
    permalink_href = find_permalink.get('href')

    # permalink has an additional bit at the start, a number, that doesn't do anything to the URL but makes it impossible to match
    # this section removes that, and then adds in the standard start of the URL
    permalink_rem = permalink_href.lstrip('https://parlinfo.aph.gov.au/43')
    stringstart = "https://parlinfo.aph.gov.au/parl"
    permalink = stringstart + permalink_rem
    key_number = key_number + 1
    unparsed_text = soup.find("div", {"class":"box"})
    unparsed_text_as_string = str(unparsed_text)

    #parse the whole text and assign to parsed_text variable
    parsed_text = remove_this_text(unparsed_text)
    stripped_text = parsed_text.strip()

    # sets up the ability to remove tables according to the functions above
    digits = "digits"
    all_tables = "all"

    # Call removing_tables function and return values for case where remove digit-based tables, and case where remove all tables
    no_digits_soup = removing_tables(digits)
    no_tables_at_all_soup = removing_tables(all_tables)

    # for each table type, find section in soup, remove the three hyperlinks at top, clean table data of new lines and additional spaces
    no_digits_find_section = no_digits_soup.find("div", {"class":"box"})
    no_digits_remove_this_text = remove_this_text(no_digits_find_section)
    text_no_digits_table = clean_table_data(no_digits_remove_this_text)

    no_tables_find_section = no_tables_at_all_soup.find("div", {"class":"box"})
    no_tables_remove_this_text =  remove_this_text(no_tables_find_section)
    text_no_tables = clean_table_data(no_tables_remove_this_text)

    cleaned_text_section = soup.find("div", {"class":"box"})
    cleaned_text_remove_this_text = remove_this_text(cleaned_text_section)
    cleaned_text = clean_table_data(cleaned_text_remove_this_text)

    #get the 'circulated by' information from the coversheet and assign to circulated_by variable
    try:
        find_circulated_parsed = re.search("\(\s*c\s*i\s*r\s*c\s*u\s*l\s*a\s*t\s*e\s*d\s.[^)]*\)", parsed_text, re.I | re.S).group()
        circulated_by = find_circulated_parsed.lower().strip()
    except:
        # replace with a searchable term and log the error in a file that can be checked
        circulated_by = "MANUAL"
        with open("exceptions_circulated_test.txt", "a") as file:
            file.write(f"{filename}\n")

    # update the row associated with the EM that you're currently parsing, via a WHERE statement that requires the document_link to be checked against the permalink established above
    cur.execute("UPDATE explanatory_memoranda SET (unparsed, parsed, circulated_by, text_no_tables, text_no_digit_tables, cleaned_text) = (?, ?, ?, ?, ?, ?) WHERE document_link = ? AND link_type = 'html';", (unparsed_text_as_string, parsed_text, circulated_by, text_no_tables, text_no_digits_table, cleaned_text, permalink))
    data = cur.fetchall()

    #commit everything
    connect_with_db.commit()

#close the connection to the database
connect_with_db.close()
