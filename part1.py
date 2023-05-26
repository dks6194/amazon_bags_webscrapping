from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import csv

def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})

        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'class': 'a-offscreen'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class': 'a-price'}).text.strip()

        except:
            price = ""

    return price


# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count





if __name__ == '__main__':
    #URL="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    page=1

    while page<21:
        URL="https://www.amazon.in/s?k=bags&page=" + str(page) + "&crid=2JDAPD2D856LD&qid=1685069008&sprefix=bags%2Caps%2C234&ref=sr_pg_2"
        HEADERS=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36','Accept-Language':'en-US, en;q=0.5'})
        webpage=requests.get(URL, headers=HEADERS)

        if(webpage=="<Response [200]>"):

            so=BeautifulSoup(webpage.content,"html.parser")
            links=so.find_all("a",attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

            links_list = []

            # Loop for extracting links from Tag Objects
            for link in links:
                links_list.append(link.get('href'))

            d = {"Product URL": [], "Product Name": [], "Product price": [], "Product rating": [], "Number of reviews": [], }

            # Loop for extracting product details from each link
            for link in links_list:
                new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

                new_soup = BeautifulSoup(new_webpage.content, "html.parser")

                # Function calls to display all necessary product information
                d['Product URL'].append("https://www.amazon.in" + link)
                d['Product Name'].append(get_title(new_soup))
                d['Product price'].append(get_price(new_soup))
                d['Product rating'].append(get_rating(new_soup))
                d['Number of reviews'].append(get_review_count(new_soup))


            amazon_df = pd.DataFrame.from_dict(d)
            amazon_df['Product Name'].replace('', np.nan, inplace=True)
            amazon_df = amazon_df.dropna(subset=['Product Name'])
            print(amazon_df)
        else:
            print("request not accepted for", page)
        #amazon_df.to_csv("amazon_data4.csv", mode='a', header=True, index=False)

        #url = "https://www.amazon.in/s?k=bags&page=" + str(page) + "&crid=2JDAPD2D856LD&qid=1685069008&sprefix=bags%2Caps%2C234&ref=sr_pg_2"
        #URL= url
        page = page + 1



