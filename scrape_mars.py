
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape():
    
    # Latest Mars News
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit browser
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.body.find("div", class_='content_title').text

    news_p = soup.body.find("div", class_='article_teaser_body').text

    url_image = 'https://spaceimages-mars.com/'
    browser.visit(url_image)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    image_div_content = soup.find("div", class_="floating_text_area")

    link = image_div_content.find('a')
    href = link['href']
    featured_image_url = url_image + href

    url_facts = 'https://galaxyfacts-mars.com/'
    browser.visit(url_facts)

    time.sleep(1)

    table = pd.read_html(url_facts, header=None, index_col=None)
    df = pd.DataFrame(table[0])

    # Renaming columns and index
    df = df.set_index(0).rename(columns={1: "Mars", 2: "Earth"})
    df.index.names = ['Description']

    html_table = df.to_html(
        classes="table table-success table-striped", bold_rows=True)

    
    # Mars Hemisphere
    url_hemispheres = 'https://marshemispheres.com/'
    browser.visit(url_hemispheres)

    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    # Hemisphere Images
    hemispheres_info = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for info in hemispheres_info:
        href_link = info.find('a')['href']
        url = url_hemispheres + href_link
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find('h2').text
        image_url = url_hemispheres + \
            soup.find('div', class_='downloads').a['href']
        hemisphere_title = soup.find('div', class_='cover').h2.text
        hemisphere_image_urls.append(
            {"title": hemisphere_title, 'img_url': image_url})

    # Store data in a dictionary
    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image_url': featured_image_url,
        'table': html_table,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
