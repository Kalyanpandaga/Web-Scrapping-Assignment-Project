import json
import sqlite3

# Connecting to sqlite
connection = sqlite3.connect('quotes.db')

#creat a cursor object
cursor_obj = connection.cursor()

def create_and_insert_values_of_authors_table(authors_details):
    # Delete the authors table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS authors")

    # Creating a authors table 
    authors_table = '''CREATE TABLE authors (
                author_id INTEGER PRIMARY KEY NOT NULL,
                name VARCHAR(255) NOT NULL,
                born_details TEXT,
                reference TEXT
            );'''
    
    cursor_obj.execute(authors_table)                                        

    # insert Data into authors table
    id = 1
    for i in range(len(authors_details)):
        if authors_details[i] not in authors_details[i+1:]:    # avoid duplicates data
            insert_values = (id, authors_details[i]['name'], authors_details[i]['born'],authors_details[i]['reference'])

            cursor_obj.execute("INSERT INTO authors VALUES (?,?,?,?)", insert_values)
            id += 1 

def get_authour_id(name):
    cursor_obj.execute('SELECT author_id FROM authors WHERE name=?', (name,))
    author_id = cursor_obj.fetchone()[0]
    return author_id
    

def create_and_insert_values_of_quotes_table(quotes_details):
    # Delete the quotes table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS quotes")

    # Creating a quotes table 
    quotes_table = '''CREATE TABLE quotes (
                quote_id INTEGER PRIMARY KEY NOT NULL,
                quote TEXT NOT NULL,
                author_name VARCHAR(255),
                author_id INTEGER,
                FOREIGN KEY(author_id) REFERENCES authors(author_id)
            );'''
    
    cursor_obj.execute(quotes_table)                                        

    # insert Data into quotes table
    id = 1
    for i in range(len(quotes_details)):
        author_id = get_authour_id(quotes_details[i]['author'])
        insert_values = (id, quotes_details[i]['quote'], quotes_details[i]['author'],author_id)

        cursor_obj.execute("INSERT INTO quotes VALUES (?,?,?,?)", insert_values)
        id += 1 


def get_all_tags_and_tag_ids_pair_list(quotes_details):
    all_tags_list = []

    for quote_obj in quotes_details:
        all_tags_list.extend(quote_obj['tags'])
        
    all_tags_unique_list = list(dict.fromkeys(all_tags_list))
    all_tag_ids_list = range(1, len(all_tags_unique_list)+1)

    merged_list = [(all_tag_ids_list[i], all_tags_unique_list[i]) for i in range(0, len(all_tag_ids_list))]
    return merged_list


def create_and_insert_values_of_tags_table(quotes_details):
    # Delete the tags table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS tags")

    # Creating a tags table 
    tags_table = '''CREATE TABLE tags (
                tag_id INTEGER PRIMARY KEY NOT NULL,
                tag VARCHAR(255) NOT NULL
            );'''
    
    cursor_obj.execute(tags_table)                                        

    # insert Data into tags table
    all_tags_and_tag_ids_merged_list = get_all_tags_and_tag_ids_pair_list(quotes_details)
    cursor_obj.executemany("INSERT INTO tags VALUES (?,?);", all_tags_and_tag_ids_merged_list)
            

def get_quote_id(quote):
    cursor_obj.execute("SELECT quote_id FROM quotes where quote = ?", (quote,))
    quote_id = cursor_obj.fetchone()[0]
    return quote_id

def get_tag_ids_list(tags_list):
    tag_ids_list = []
    for each_tag in tags_list:
        cursor_obj.execute("SELECT tag_id FROM tags where tag = ?", (each_tag,))
        tag_ids_list.append(cursor_obj.fetchone()[0])
    return tag_ids_list
     

def get_quote_ids_and_tag_ids_merged_list(quote_dict):
    quote = quote_dict['quote']
    quote_id = get_quote_id(quote)

    tags_list = quote_dict['tags']
    tag_ids_list = get_tag_ids_list(tags_list)

    quote_ids_and_tag_ids_merged_list = [(quote_id, tag_ids_list[i]) for i in range(0, len(tag_ids_list))]
    return quote_ids_and_tag_ids_merged_list



def create_and_insert_values_of_quote_tag_table(quotes_details):
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
create_and_insert_values_of_authors_table(authors_details)
connection.commit() #commit the changes in db

create_and_insert_values_of_quotes_table(quotes_details)
connection.commit()

create_and_insert_values_of_tags_table(quotes_details)
connection.commit()

create_and_insert_values_of_quote_tag_table(quotes_details)
connection.commit()

# Close the connection
connection.close()
        