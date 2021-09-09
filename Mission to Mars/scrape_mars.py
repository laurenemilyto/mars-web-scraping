# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager 
import pandas as pd
import time
import lxml

def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
## NASA Mars News
    # NASA Mars News URL of page to be scraped
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Identify and return latest news title
    results = news_soup.find_all('div', class_="content_title")
    news_title = results[1].text

    # Identify and return latest paragraph text
    results = news_soup.find_all('div', class_="article_teaser_body")
    news_p = results[0].text

## JPL Mars - Featured Image
    browser = Browser('chrome', **executable_path, headless=False)
    space_image_url = "https://spaceimages-mars.com/"

    # Use Beautiful Soup to parse HTMl via the browser
    browser.visit(space_image_url)

    # Suspend execution for 1 second
    time.sleep(1)

    # Scrape page into Soup
    image_soup = bs(html,'html.parser')

    # Get featured image url
    featured_image_url = image_soup.find_all("img")[1]["src"]

## Pandas Scraping: Mars Facts
    facts_url = 'https://galaxyfacts-mars.com/'
    mars_facts = pd.read_html(facts_url)
    facts_df = mars_facts[0]
    facts_df.columns = ["Properties", "Mars", "Earth"]
    facts_df = facts_df.set_index("Properties")
    facts_df

    # Convert data to a HTML table string. 
    mars_facts = facts_df.to_html()

## Mars Hemispheres
    # Setup splinter
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    html = browser.html
    astro_soup = bs(html, 'html.parser')

    # Extract Results where class = collapsible results
    mars_hems = astro_soup.find("div", class_="collapsible results")
    results = mars_hems.find_all('div', class_="item")

    # Create empty list for images
    hemisphere_images = []

    # Loop through results
    for result in results:
        # Error handling
        try:
            # Use bs to find title
            title = astro_soup.find('h3').text.strip()
            # Use bs to find and create image link
            href = result.find('a')['href']
            browser.visit(hemispheres_url + href)
            html = browser.html
            src_soup = bs(html, 'html.parser')
            image_link = src_soup.find('div', class_='downloads')
            image_url = image_link.find('li').a['href']
            full_path = hemispheres_url + image_url
            # Append title and image URL to dict
            hemisphere_images.append({"title":title,"img_url":full_path})
        except Exception as e:
            print(e)

    ## Save Scraped Data
    mars_dict = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "mars_facts":mars_facts,
        "hemisphere_images":hemisphere_images
    }

    # Close the browser after scraping
    browser.quit() 

    ## Return results
    print(mars_dict)
    return mars_dict

if __name__ == "__main__":
    scrape()