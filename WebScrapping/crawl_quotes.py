def get_quote_dict(quotes_element):
    quote_dict = dict()

    quote_dict['quote'] = quotes_element.find("span", class_="text").text.strip('“,”')
    quote_dict['author'] = quotes_element.find("small", class_="author").text

    tags_container_element = quotes_element.find("div", class_="tags")

    tag_elements = tags_container_element.find_all("a", class_="tag")

    # print(tag_elements);

    tags = []
    for tag_element in tag_elements:
        tags.append(tag_element.text)
    
    quote_dict['tags'] = tags
    return quote_dict

def get_author_dict(quotes_element):
    author_dict = dict()

    author_dict['name'] = quotes_element.find("small", class_="author").text

    author_details_container =quotes_element.find_all("span")[1]
    author_page_url = author_details_container.find("a")['href']
    author_page_url = main_url + author_page_url

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
main_url = 'http://quotes.toscrape.com'


quotes = []
authors = []
def web_scrapping(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.content, 'html.parser')

    quotes_elements = soup.find_all("div", class_="quote")

    
    for quotes_element in quotes_elements:
        quotes.append(get_quote_dict(quotes_element))
        authors.append(get_author_dict(quotes_element))
    
    next_elememt = soup.find("li", class_="next")
    if next_elememt == None:
        return
    page_url = next_elememt.find('a')['href']
    url = main_url + page_url
    web_scrapping(url)

url = main_url       
web_scrapping(url)

dict_of_quotes_and_author = {"quotes":quotes, "authors":authors}

string_format_of_dict_obj = json.dumps(dict_of_quotes_and_author, indent=4)

json_file = open('quotes.json','w')
json_file.write(string_format_of_dict_obj)
json_file.close()

