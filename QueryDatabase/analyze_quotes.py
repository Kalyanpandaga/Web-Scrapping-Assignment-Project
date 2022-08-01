import sqlite3

# Connecting to sqlite
connection = sqlite3.connect('../CreateDatabase/quotes.db')
  
# cursor object
cursor_obj = connection.cursor()

# create function that return the total no.of quotes in website 
def get_total_no_of_quotes():
    statement = '''SELECT count(quote_id) as total_quotes FROM quotes;'''
    cursor_obj.execute(statement)
    total_quotes = cursor_obj.fetchone()[0]
    return total_quotes


# create a function that return No. of quotations authored by the given author’s name
def get_no_of_quotes_authored_by_author(author_name):
    statement = '''SELECT count(quote_id) as number_of_quotes FROM quotes where author_name = ?;'''
    cursor_obj.execute(statement, (author_name,))
    number_of_quotes_by_given_author = cursor_obj.fetchone()[0]
    return number_of_quotes_by_given_author


# create a function that return Minimum, Maximum, and Average no. of tags on the quotations
def get_min_max_avg_no_of_tags():
    statement = '''SELECT COUNT(tag_id) As no_of_tags FROM quotes LEFT JOIN quote_tag ON quotes.quote_id = quote_tag.quote_id 
                GROUP BY quotes.quote_id'''
    cursor_obj.execute(statement)
    query_result = cursor_obj.fetchall()

    no_of_tags_list = []
    for each_tuple in query_result:
        no_of_tags_list.extend(each_tuple)
    
    minimum = min(no_of_tags_list)
    maximum = max(no_of_tags_list)
    average = sum(no_of_tags_list)/len(no_of_tags_list)

    return {"min_no_of_tags":minimum, "max_no_of_tags": maximum, "avg_no_of_tags":average}


# create a function that return top N authors who authored the maximum number of quotations
def get_authors_who_authored_maxmimum_no_of_quotations(n):
    statement = '''SELECT author_name, COUNT() as no_of_quotes FROM 'quotes' GROUP BY author_id ORDER BY no_of_quotes DESC LIMIT ?;'''
    cursor_obj.execute(statement, (n,))
    top_n_authors_list_of_tuples = cursor_obj.fetchall()

    top_n_authors = []
    for author_tuple in top_n_authors_list_of_tuples:
        top_n_authors.append(author_tuple[0])

    return tuple(top_n_authors)

# call the above functions
print(get_total_no_of_quotes())
connection.commit() # commit the changes in db

print(get_no_of_quotes_authored_by_author("Albert Einstein"))
connection.commit()

print(get_min_max_avg_no_of_tags())
connection.commit()

print(get_authors_who_authored_maxmimum_no_of_quotations(5))
connection.commit()

# Close the connection
connection.close() 