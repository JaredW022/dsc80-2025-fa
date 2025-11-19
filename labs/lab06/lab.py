# lab.py


import os
import pandas as pd
import numpy as np
import requests
import bs4
import lxml


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def question1():
    """
    NOTE: You do NOT need to do anything with this function.
    The function for this question makes sure you
    have a correctly named HTML file in the right
    place. Note: This does NOT check if the supplementary files
    needed for your page are there!
    """
    # Don't change this function body!
    # No Python required; create the HTML file.
    return


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------



def extract_book_links(text):
    soup = bs4.BeautifulSoup(text, 'lxml')
    books = soup.find_all("li", attrs={"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
    prices = [(float)(books[i].find("p", attrs={"class": "price_color"}).text.replace("£", "").replace("Â", "")) for i in range(len(books))]
    text_to_nums = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    star_ratings = [(text_to_nums.get(books[i].find("p", attrs={"class": "star-rating"}).get("class")[1])) for i in range(len(books))]
    titles = [books[i].find("h3").find("a").get("title") for i in range(len(books))]
    links = [books[i].find("h3").find("a").get("href") for i in range(len(books))]
    df = pd.DataFrame({"star ratings": star_ratings, "prices": prices, "href": links}, index=titles)
    return list(df[(df["star ratings"] >= 4) & (df["prices"] <50)]["href"].values)

def get_product_info(text, categories):
    soup = bs4.BeautifulSoup(text, 'lxml')
    tables = soup.find("table")
    lst = []
    table_tr = tables.find_all("tr")
    for row in table_tr:
        lst.append(row.find("td").text)
    category = soup.find("ul", attrs={"class": "breadcrumb"}).find_all("a")[-1].text
    star_rating = soup.find("div", attrs={"class": "col-sm-6 product_main"}).find("p", attrs={"class": "star-rating"}).get("class")[1]
    description = soup.find("meta", attrs={"name": "description"}).get("content").strip()
    title = soup.find("div", attrs={"class": "col-sm-6 product_main"}).find("h1").text
    lst.extend([category, star_rating, description, title])
    col_names = ["UPC", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "Availability", "Number of reviews", "Category", "Rating", "Description", "Title"]
    dct = dict(zip(col_names, lst))
    if dct.get("Category") in categories:
        return dct
    else:
        return None

def scrape_books(k, categories):
    pages = []
    for i in range(1, k + 1):
        response = requests.get(f"https://books.toscrape.com/catalogue/page-{i}.html")
        pages.append(response.text)
    links = []
    for page in pages:
        links.extend(extract_book_links(page))
    rows = []
    for link in links:
        response2 = requests.get(f"https://books.toscrape.com/catalogue/{link}").text
        rows.append(get_product_info(response2, categories))
    valid_rows = []
    for row in rows:
        if row != None:
            valid_rows.append(row)
    return pd.DataFrame(valid_rows)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def get_comments(storyid):

    def get_current_info(id):
        response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json").json()
        if response.get("dead") or response.get("deleted"):
            return []

        current_id = response.get("id")
        by = response.get("by")
        text = response.get("text")
        parent = response.get("parent")
        time = pd.to_datetime(response.get("time"), unit='s')

        temp = [[current_id, by, text, parent, time]]

        kids = response.get("kids")
        if response.get("kids") != None:
            for kid in kids:
                temp.extend(get_current_info(kid))
            return temp
        else:
            return temp
        
    data = get_current_info(storyid)
    cols = ["id", "by", "text", "parent", "time"]
    return pd.DataFrame(data[1:], columns=cols)