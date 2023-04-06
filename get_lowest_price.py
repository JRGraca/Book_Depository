import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup
from random import randint
from time import sleep

wishlist = pd.read_csv('wishlist.csv', delimiter=';')
wishlist.drop(columns='Notes', inplace=True)
#BOOK DEPOSITORY

#Since I'm assuming the input is a Book Depository wishlist, I don't include error handling for the case in which the book might not exist in the database.
#As I write this, I realize I probably should, because of Murphy's Law, but this code will only be valid for a few weeks, anyway, so nah

price_list_bd = []

for item in wishlist['ISBN']:
    url = r'https://www.bookdepository.com/isbn/' + str(item)
    print("Scraping... " + str(item))
    html = rq.get(url)
    if html.status_code != 200:
        print("Page not read")
        break
    else:
        soup = BeautifulSoup(html.content)
        test_if_there_is_price = soup.find("span", class_ = "sale-price")
        if test_if_there_is_price is None: #There is no "sale-price" class - this means the book is out of stock
            price = np.nan
        else: #Otherwise, finds the price and processes it to convert it to a numeric value. Assumes price is in €uros
            price_string = soup.find("span", class_ = "sale-price").text
            price = float(price_string.replace(",", ".")[:-2])
    price_list_bd.append(price)
    print("Price is ", price)
    # Waits a few seconds to simulate a user clicking around
    time_to_sleep = randint(1,6)
    print("Sleeping for " + str(time_to_sleep) + " seconds...")
    sleep(time_to_sleep)
wishlist['Price_BD'] = pd.Series(price_list_bd)
        
#BLACKWELL'S

price_list_bw = []

for item in wishlist['ISBN']:
    url = 'https://blackwells.co.uk/bookshop/product/' + str(item)
    print("Scraping... " + str(item))
    html = rq.get(url)
    if html.status_code != 200: # Status code different from 200 means request was not successful
        print(f"Page not read - {item}")
        price = np.nan
    else:
        soup = BeautifulSoup(html.content)
        if soup.find_all(string="Not available for sale") == []: #If the book is available for sale, the string will not exist, so we can check the price
            price_string = soup.find("li", class_="product-price--current")
            #The site will generate pages based on any valid isbn you write, however, if they don't have it in the database the page will be blank.
            #In that case, the string test above will not show a problem, so we have to test if the <li> tag actually exists (ie, the book exists in the database)
            if price_string is None: 
                price = np.nan
                print(f"Book not in catalogue - " + str(item))
            else: #When the book exists in the database, this will process the price to a useful format. Assumes price is in €uros
                price = float(price_string.text.strip().replace(",", ".")[:-1])
        else: #Book in catalogue, but out of stock
            price = np.nan
    price_list_bw.append(price)
    print("Price is ", price)
    # Waits a few seconds to simulate a user clicking around
    time_to_sleep = randint(1,6)
    print("Sleeping for " + str(time_to_sleep) + " seconds...")
    sleep(time_to_sleep)
wishlist['Price_BW'] = pd.Series(price_list_bw)

#This will create two tables, one for each bookshop. In each of those tables are all books which are cheaper in that particular bookshop and
#also all books which are not available in the other bookshop, sorted by price (cheapest first)

BW_books = wishlist[(wishlist['Price_BW'] < wishlist['Price_BD']) | (wishlist['Price_BD'].isna())].sort_values(by='Price_BW')

BD_books = wishlist[(wishlist['Price_BW'] > wishlist['Price_BD']) | (wishlist['Price_BW'].isna())].sort_values(by='Price_BD')

#This prints out the recommendation of what books to buy. The logic is whatever the cheapest book in your wishlist is, *UNLESS* it's cheaper in the other bookstore

print(f'Recommended book to buy at Blackwell\'s is {BW_books.iloc[0][2]} by {BW_books.iloc[0][3]}, ISBN {BW_books.iloc[0][1]} for €{BW_books.iloc[0][5]}')

print(f'Recommended book to buy at the Book Depository is {BD_books.iloc[0][2]} by {BD_books.iloc[0][3]}, ISBN {BD_books.iloc[0][1]} for €{BD_books.iloc[0][4]}')

