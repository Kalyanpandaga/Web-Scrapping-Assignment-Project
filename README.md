# Web-Scrapping-Assignment-Project

Use Python to:

1.browse and extract specific data from a website

2.store this information in a database and

3.query the database to answer specific questions about the crawled data.
 

Accordingly, this assignment is broken down into 3 questions. Each question builds on top of the previous one. 
For each question, we’re required to write Python code. 

step 1:

Scrape quotes data from the website  http://quotes.toscrape.com/ using a Python script and write the complete information 
into a JSON file.

In this program, we are using Beautiful Soup. Beautiful Soup is a Python library for pulling data out of HTML and XML files. 
This Beautiful Soup module is not a predefined module in python.

so we installing this using PIP(Preferred Installer Program). 

Guidelines to Install Beautiful Soup 4 :

If you’re using a recent version of Debian or Ubuntu Linux, you can install Beautiful Soup with the system package manager:

$ apt-get install python-bs4 (for Python 2)

$ apt-get install python3-bs4 (for Python 3)

Beautiful Soup 4 is published through PyPi, so if you can’t install it with the system packager, you can install it with easy_install or pip. 
The package name is beautifulsoup4, and the same package works on Python 2 and Python 3. Make sure you use the right version of pip or easy_install
for your Python version (these may be named pip3 and easy_install3 respectively if you’re using Python 3).

$ easy_install beautifulsoup4

$ pip install beautifulsoup4


step 2:

Store the data scraped in the previous question in an SQLite database using a Python script. 

Create the tables using Quotes, Authors, and Tags to appropriately store the information.
  
Use foreign keys to maintain relationships among different tables.
  
Define table schema so that the data duplication is minimized.


Step 3 :

In this program we write python functions that execute the SQL queries to answer the below questions.

1. Return Total no. of quotations on the website

2. Return No. of quotations authored by the given author’s name
   Example: “Albert Einstein”

3. Return Minimum, Maximum, and Average no. of tags on the quotations

4. Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes


