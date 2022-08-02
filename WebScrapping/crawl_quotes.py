
def get_quote_dict(quotes_element):
    quote_dict = dict()

    # selecting quotation and author_names from website and 
    # add to the quote_dict with using keys 'quote', 'author' 
    quote_dict['quote'] = quotes_element.find("span", class_="text").text.strip('“,”') 
    quote_dict['author'] = quotes_element.find("small", class_="author").text

    # selecting tag elements from website and add list of tags to the quote_dict dictionary
    tags_container_element = quotes_element.find("div", class_="tags")

    tag_elements = tags_container_element.find_all("a", class_="tag")

    tags = []
    for tag_element in tag_elements:
        tags.append(tag_element.text)
    
    quote_dict['tags'] = tags
    return quote_dict

def get_author_dict(quotes_element):
    author_dict = dict()

    # selecting author_names from website and adding to the author_dict
    author_dict['name'] = quotes_element.find("small", class_="author").text

    # find and take the author page url
    author_details_container =quotes_element.find_all("span")[1]
    author_page_url = author_details_container.find("a")['href']
    author_page_url = main_url + author_page_url 

    # request to the author page
    author_html_doc = requests.get(author_page_url)

    soup_aut = BeautifulSoup(author_html_doc.content, 'html.parser')

    born_date = soup_aut.find("span", class_="author-born-date").text
    born_location = soup_aut.find("span", class_="author-born-location").text
    born_date_and_location = born_date +" "+ born_location

    author_dict['born'] = born_date_and_location 
    author_dict['reference'] = author_page_url

    return author_dict


import requests
import json
from bs4 import BeautifulSoup
# BeautifulSoup is used to take html content to the web page
main_url = 'http://quotes.toscrape.com'


quotes = []  # we append all quotation details in this list
authors = [] # we append all authors details in this list
def web_scrapping(url):
    # requesting to the web page
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    quotes_elements = soup.find_all("div", class_="quote")

    
    for quotes_element in quotes_elements:
        quotes.append(get_quote_dict(quotes_element))
        authors.append(get_author_dict(quotes_element))

    # using recursive function to Crawling Data from multiple web pages
    next_elememt = soup.find("li", class_="next")

    if next_elememt == None:
        return
    page_url = next_elememt.find('a')['href']
    url = main_url + page_url
    web_scrapping(url)

url = main_url       
web_scrapping(url)

dict_of_quotes_and_author = {"quotes":quotes, "authors":authors}

# converting python dict to string format of json object
string_format_of_dict_obj = json.dumps(dict_of_quotes_and_author, indent=4)

# adding json text to the json file by using File-handling

json_file = open('quotes.json','w')        # open json file using open() method
json_file.write(string_format_of_dict_obj) # write the json text in file using write() method
json_file.close()                          # close the file using close() method

