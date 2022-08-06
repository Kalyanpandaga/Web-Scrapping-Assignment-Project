import json
import sqlite3

# Connecting to sqlite
connection = sqlite3.connect('quotes.db')

#creat a cursor object
cursor_obj = connection.cursor()

def create_author_table():
    # Delete the author table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS author")

    # Creating a authors table 
    author_table = '''CREATE TABLE author (
                author_id INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL,
                born_details TEXT,
                reference TEXT
            );'''
    
    cursor_obj.execute(author_table)                                        


def insert_values_of_author_table(authors_details):                                       
    # insert Data into author table
    for i in range(len(authors_details)):
        insert_values = (i+1, authors_details[i]['name'], authors_details[i]['born'],authors_details[i]['reference'])
        cursor_obj.execute("INSERT INTO author VALUES (?,?,?,?)", insert_values)

def create_quote_table():
    # Delete the quote table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS quote")

    # Creating a quote table 
    quote_table = '''CREATE TABLE quote (
                quote_id INTEGER PRIMARY KEY NOT NULL,
                quote TEXT NOT NULL,
                author_id INTEGER,
                FOREIGN KEY(author_id) REFERENCES authors(author_id)
            );'''
    
    cursor_obj.execute(quote_table)   


def get_author_id(name):
    cursor_obj.execute('SELECT author_id FROM author WHERE name=?', (name,))
    author_id = cursor_obj.fetchone()[0]
    return author_id
    
def insert_values_of_quote_table(quotes_details):                                       
    # insert Data into quote table
    for i in range(len(quotes_details)):
        author_id = get_author_id(quotes_details[i]['author'])
        insert_values = (i+1, quotes_details[i]['quote'], author_id)

        cursor_obj.execute("INSERT INTO quote VALUES (?,?,?)", insert_values)
         

def create_tag_table():
    # Delete the tag table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS tag")

    # Creating a tag table 
    tag_table = '''CREATE TABLE tag (
                tag_id INTEGER PRIMARY KEY NOT NULL,
                tag VARCHAR(255) NOT NULL
            );'''
    
    cursor_obj.execute(tag_table) 

def get_all_tags_and_tag_ids_pair_list(quotes_details):
    all_tags_list = []

    for quote_obj in quotes_details:
        all_tags_list.extend(quote_obj['tags'])
        
    all_tags_unique_list = list(dict.fromkeys(all_tags_list))
    all_tag_ids_list = range(1, len(all_tags_unique_list)+1)

    merged_list = [(all_tag_ids_list[i], all_tags_unique_list[i]) for i in range(0, len(all_tag_ids_list))]
    return merged_list

def insert_values_of_tag_table(quotes_details):                                        
    # insert Data into tags table
    all_tags_and_tag_ids_merged_list = get_all_tags_and_tag_ids_pair_list(quotes_details)
    cursor_obj.executemany("INSERT INTO tag VALUES (?,?);", all_tags_and_tag_ids_merged_list)


def create_quote_tag_table():
    # Delete the quote_tag table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS quote_tag")

    # Creating a quote_tag table 
    quote_tag_table = '''CREATE TABLE quote_tag (
                quote_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                FOREIGN KEY(quote_id) REFERENCES quotes(quotes_id),
                FOREIGN KEY(tag_id) REFERENCES tags(tags_id)
            );'''
    
    cursor_obj.execute(quote_tag_table)          

def get_quote_id(quote):
    cursor_obj.execute("SELECT quote_id FROM quote where quote = ?", (quote,))
    quote_id = cursor_obj.fetchone()[0]
    return quote_id

def get_tag_ids_list(tags_list):
    tag_ids_list = []
    for each_tag in tags_list:
        cursor_obj.execute("SELECT tag_id FROM tag where tag = ?", (each_tag,))
        tag_ids_list.append(cursor_obj.fetchone()[0])
    return tag_ids_list
     

def get_quote_ids_and_tag_ids_merged_list(quote_dict):
    quote = quote_dict['quote']
    quote_id = get_quote_id(quote)

    tags_list = quote_dict['tags']
    tag_ids_list = get_tag_ids_list(tags_list)

    quote_ids_and_tag_ids_merged_list = [(quote_id, tag_ids_list[i]) for i in range(0, len(tag_ids_list))]
    return quote_ids_and_tag_ids_merged_list



def insert_values_of_quote_tag_table(quotes_details):                                        
    # insert Data into quote_tag table
    for i in range(len(quotes_details)):
        quote_ids_and_tag_ids_merged_list = get_quote_ids_and_tag_ids_merged_list(quotes_details[i])
        cursor_obj.executemany("INSERT INTO quote_tag VALUES (?,?);", quote_ids_and_tag_ids_merged_list)


# open json file and convert dict object
file = open("../WebScrapping/quotes.json", "r")
json_file = file.read() 

quotes_and_author_dict = json.loads(json_file)

quotes_details = quotes_and_author_dict['quotes']
authors_details = quotes_and_author_dict['authors']

# call the above functions
create_author_table()
connection.commit() #commit the changes in db

insert_values_of_author_table(authors_details)
connection.commit()

create_quote_table()
connection.commit()

insert_values_of_quote_table(quotes_details)
connection.commit()

create_tag_table()
connection.commit()

insert_values_of_tag_table(quotes_details)
connection.commit()

create_quote_tag_table()
connection.commit()

insert_values_of_quote_tag_table(quotes_details)
connection.commit()
# Close the connection
connection.close()
        