from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
#import pymongo

mars_data = {}

def init_browser():

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

def scrape_nasa_info():
    browser = init_browser()
    
    url = "https://mars.nasa.gov/news/" 
    browser.visit(url)
    time.sleep(5)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("div", class_='list_text')
    news_title = article.find('div', class_="content_title").find('a').text
    news_p = article.find('div',class_="article_teaser_body").text
    
    nasa_data = {"news_title":news_title,
                "news_p":news_p}
    browser.quit()
    
    mars_data["nasa_data"]=nasa_data
    return nasa_data

def scrape_jpl_info():
    browser = init_browser()
    
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" 
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    relative_image_path = soup.find("article", class_="carousel_item").find("footer").find("a")["data-fancybox-href"]
    featured_image_url = url + relative_image_path
    
    browser.quit()
    
    mars_data["featured_image_url"] = featured_image_url
    return featured_image_url

##INSERT TWITTER WEATHER DATA HERE
def scrape_mars_weather():
    browser = init_browser()

    weather_url = 'https://twitter.com/marswxreport'
    browser.visit(weather_url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_weather = soup.find('body').find("main").find("article").find_all("span")[4].text
    mars_weather = mars_weather.replace("\n"," ")

    mars_data["mars_weather"] = mars_weather
    return mars_weather


##Mars Facts
#use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

def scrape_mars_facts():
    facts_url = 'https://space-facts.com/mars/'
    mars_df = pd.read_html(facts_url)[0]
    mars_df.columns = ["Description", "Value"]
    
    mars_html = mars_df.to_html()
    mars_html = mars_html.replace('\n', '')
    
    mars_data["mars_html"] = mars_html
    return mars_html

##Mars Hemispheres
# Mars hemisphere name and image to be scraped
def scrape_mars_hemispheres():

    browser = init_browser()
    base_url = 'https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemispheres_url)

    hemispheres_html = browser.html

    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
    
    all_mars_hemispheres = hemispheres_soup.find('div', class_='result-list')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

    # Collect all data per hemisphere
    for hemisphere in mars_hemispheres:

        # Collect Titles
        hemisphere = hemisphere.find('div', class_="description")
        title = hemisphere.h3.text

        # Collect image links
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(base_url + hemisphere_link)

        image_html = browser.html
        image_soup = BeautifulSoup(image_html, 'html.parser')

        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Store in dictionary
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url

        hemisphere_image_urls.append(image_dict)

    browser.quit()
    
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    return hemisphere_image_urls