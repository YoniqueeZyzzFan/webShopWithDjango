from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import random


def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string


def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
        except:
            price = ""
    return price


def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating


def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count


def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available


def generate_user_agent():
    platform = random.choice(['Macintosh', 'Windows', 'X11'])
    browser = random.choice(['Chrome', 'Firefox', 'Safari'])
    version = '.'.join(str(random.randint(0, 9)) for _ in range(3))
    user_agent = f"Mozilla/5.0 ({platform}; {browser}/{version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36"
    return user_agent


def scrapping(base_url, file_name):
    headers = {
        'User-Agent': generate_user_agent(),
        'Accept-Language': 'en-US,en; q=0.9',
    }
    d = {"title": [], "price": [], "rating": [], "reviews": [], "image_link": []}
    page_num = 1
    while page_num <= 2:
        url = base_url.format(page_num)
        webpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
        if len(links) == 0:
            break
        links_list = []
        for link in links:
            links_list.append(link.get('href'))
        for link in links_list:
            new_webpage = requests.get("https://www.amazon.com" + link, headers=headers)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")
            d['title'].append(get_title(new_soup))
            price_element = new_soup.find("span", class_="a-offscreen")
            price = price_element.text.strip()
            if '$' in price:
                d['price'].append(price)
            else:
                d['price'].append('N/A')
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            image_element = new_soup.find("div", attrs={'id': 'imgTagWrapperId'})
            image_link = image_element.find("img")['src'] if image_element and image_element.find("img") else 'no image'
            d['image_link'].append(image_link)
        page_num += 1
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv(file_name + '.csv', header=True, index=False)


if __name__ == '__main__':
    urls = [
        f'https://www.amazon.com/s?bbn=16225009011&rh=n%3A667846011&dc&qid=1688499750&rnid=16225009011&ref=lp_16225009011_nr_n_6',
        f'https://www.amazon.com/s?bbn=16225009011&rh=n%3A541966&dc&qid=1688505202&rnid=16225009011&ref=lp_16225009011_nr_n_4']
    file_names = ['home_audio', 'computer_accessories']
    for i in range(len(urls)):
        scrapping(urls[i], file_names[i])
