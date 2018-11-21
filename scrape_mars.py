
# coding: utf-8


# Dependencies
import os
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import time
import pandas as pd


def init_browser():
    
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)




def scrape():

    browser = init_browser()
    mars_data_dict = {}



    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html



    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    

    mars_data_dict["title"] = news_title
    mars_data_dict["para"] = news_p


    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_image)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    
    time.sleep(3)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    time.sleep(3)

    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    
    results = soup.find('article')
    image = results.find('figure', 'lede').a['href']
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + image

    mars_data_dict["feat"] =  featured_image_url
    

   
    


    
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)

    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    recent_tweet = soup.find('ol', class_='stream-items')
    mars_weather = recent_tweet.find('p', class_="tweet-text").text
    
    mars_data_dict["weather"] = mars_weather
   
    


    url_facts= "https://space-facts.com/mars/"
    browser.visit(url_facts)

    table = pd.read_html(url_facts)
    table_df = pd.DataFrame(table[0])
    html_table = table_df.to_html()
    

    mars_data_dict["facts"] = html_table
    


    url_hemis = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemis)

    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    for i in range (4):
        time.sleep(3)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find('div', 'downloads').a['href']
        title = soup.find("h2",class_="title").text
        dictionary={"title":title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()


    mars_data_dict["hemis"] = hemisphere_image_urls


    # Close the browser after scraping
    browser.quit()

    return mars_data_dict
    

