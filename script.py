import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import requests

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


def search(product):
    df_pickaboo = pickaboo_search(product)
    df_priyoshop = priyoshop_search(product)
    df_rayans = rayans_search(product)
    df_startech = startech_search(product)
    #df_techland = techland_search(product)
    #df_computersource = computersource_search(product)

    frames = [df_rayans, df_startech, df_priyoshop, df_pickaboo]
    df = pd.concat(frames,ignore_index=True)
    df.to_json('static/pickaboo.json')


def pickaboo_search(product):
    result = requests.get("https://www.pickaboo.com/catalogsearch/result/?q="+product)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    #scrape image, name, link, price html tag
    product_images = soup.find_all('img', attrs={'class': 'product-image-photo'})
    product_images = list(dict.fromkeys(product_images))

    product_names = soup.find_all('strong', attrs={'class': 'product name product-item-name'})

    product_prices =  soup.find_all('span', attrs={'data-price-type': 'finalPrice'})

    product_links = soup.find_all('a', attrs={'class': 'product-item-link'})

    #grabe image, name price information
    product_name_only = []
    for product_name in product_names:
        product_name_only.append(product_name.text.strip())


    product_price_only = []
    for product_price in product_prices:
        product_price_only.append(product_price.text.strip())


    product_image_only = []
    for product_image in product_images:
        product_image_only.append(product_image.attrs['src'])

    product_link_only = []
    for product_link in product_links:
        product_link_only.append(product_link.attrs['href'])

    #convert list to separate dataframe
    df_img = pd.DataFrame({'image':product_image_only})
    df_name = pd.DataFrame({'name':product_name_only})
    df_price = pd.DataFrame({'price':product_price_only})
    df_link = pd.DataFrame({'link':product_link_only})


    #marge all dataframe
    df = pd.concat([df_img,df_name,df_price,df_link], axis=1)
    df['icon'] = 'https://b2b-pickaboocdn.s3-ap-southeast-1.amazonaws.com/media/logo/stores/1/pickaboo-logo.png'
    
    return df






def priyoshop_search(product):  
    result = requests.get("https://priyoshop.com/src?q="+product)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    #scrape image, name, link, price html tag
    product_images = soup.find_all('div', attrs={'class': 'picture'})
    product_names = soup.find_all('h2', attrs={'class': 'product-title'})
    product_prices =  soup.find_all('span', attrs={'class': 'price actual-price'})
    product_links = soup.find_all('div', attrs={'class': 'picture'})

    #grabe image, name price information
    product_name_only = []
    for product_name in product_names:
        product_name_only.append(product_name.text.strip())


    product_price_only = []
    for product_price in product_prices:
        product_price_only.append(product_price.text.strip())


    product_image_only = []
    for product_image in product_images:
        product_image_only.append(product_image.img.attrs['src'])

    product_link_only = []
    for product_link in product_links:
        product_link_only.append('https://priyoshop.com'+product_link.a.attrs['href'])

    #convert list to separate dataframe
    df_img = pd.DataFrame({'image':product_image_only})
    df_name = pd.DataFrame({'name':product_name_only})
    df_price = pd.DataFrame({'price':product_price_only})
    df_link = pd.DataFrame({'link':product_link_only})


    #marge all dataframe
    df = pd.concat([df_img,df_name,df_price,df_link], axis=1)
    df['icon'] = 'https://s3-ap-southeast-1.amazonaws.com/priyoshop/content/Images/thumbs/0072813.png'
    
    return df



def rayans_search(product):
    
    def render_page(url):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        #driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(3)
        r = driver.page_source
        #driver.quit()
        return r

    result = render_page('https://www.ryanscomputers.com/search?q='+product)
    soup = BeautifulSoup(result, "html.parser")




    product_images = soup.find_all('div', attrs={'class': 'product-thumb'})
    product_names = soup.find_all('div', attrs={'class': 'product-thumb'})
    product_prices =  soup.find_all('span', attrs={'class': 'price'})
    product_links = soup.find_all('div', attrs={'class': 'product-thumb'})


    product_image_only = []
    for product_image in product_images:
        product_image_only.append(product_image.img.attrs['src'])

    product_name_only = []
    for product_name in product_names:
        product_name_only.append(product_name.img.attrs['alt'])

    product_price_only = []
    for product_price in product_prices:
        product_price_only.append(product_price.text.strip())

    product_link_only = []
    for product_link in product_links:
        product_link_only.append(product_link.a.attrs['href'])

    df_img = pd.DataFrame({'image':product_image_only})
    df_name = pd.DataFrame({'name':product_name_only})
    df_price = pd.DataFrame({'price':product_price_only})
    df_link = pd.DataFrame({'link':product_link_only})

    df = pd.concat([df_img,df_name,df_price,df_link], axis=1)
    df['icon'] = 'https://www.ryanscomputers.com/assets/website/img/ryans-computers.svg'

    return df



def startech_search(product):
    result = requests.get("https://www.startech.com.bd/product/search?search="+product)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')


    product_images = soup.find_all('div', attrs={'class': 'img-holder'})
    product_names = soup.find_all('h4', attrs={'class': 'product-name'})
    product_prices =  soup.find_all('div', attrs={'class': 'price'})
    product_links = soup.find_all('h4', attrs={'class': 'product-name'})

    product_image_only = []
    for product_image in product_images:
        product_image_only.append(product_image.img.attrs['src'])

    product_name_only = []
    for product_name in product_names:
        product_name_only.append(product_name.a.text.strip())

    product_price_only = []
    for product_price in product_prices:
        product_price_only.append(product_price.span.text.strip())


    product_link_only = []
    for product_link in product_links:
        product_link_only.append(product_link.a.attrs['href'])

    df_img = pd.DataFrame({'image':product_image_only})
    df_name = pd.DataFrame({'name':product_name_only})
    df_price = pd.DataFrame({'price':product_price_only})
    df_link = pd.DataFrame({'link':product_link_only})

    df = pd.concat([df_img,df_name,df_price,df_link], axis=1)
    df['icon'] = 'https://www.startech.com.bd/image/catalog/logo.png'

    return df




def techland_search(product):
    result = requests.get("https://www.techlandbd.com/index.php?route=product/search&search="+product)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    product_images = soup.find_all('a', attrs={'class': 'product-img'})
    product_names = soup.find_all('div', attrs={'class': 'name'})
    product_prices =  soup.find_all('span', attrs={'class': 'price-tax'})
    product_links = soup.find_all('div', attrs={'class': 'name'})



    product_image_only = []
    for product_image in product_images:
        product_image_only.append(product_image.img.attrs['data-src'])

    product_name_only = []
    for product_name in product_names:
        product_name_only.append(product_name.a.text.strip())

    product_price_only = []
    for product_price in product_prices:
        product_price_only.append(product_price.text.strip().replace('Ex Tax:', ''))

    product_link_only = []
    for product_link in product_links:
        product_link_only.append(product_link.a.attrs['href'])


    df_img = pd.DataFrame({'image':product_image_only})
    df_name = pd.DataFrame({'name':product_name_only})
    df_price = pd.DataFrame({'price':product_price_only})
    df_link = pd.DataFrame({'link':product_link_only})

    df = pd.concat([df_img,df_name,df_price,df_link], axis=1)
    df['icon'] = 'https://www.techlandbd.com/image/cache/catalog/techland/logo/techland-logo-white-300-300x48.png'

    return df



def computersource_search(product):
    result = requests.get("https://www.computersourcebd.com/search?q="+product)
    src = result.content
    soup = BeautifulSoup(src, 'lxml')

    product_images = soup.find_all('img', attrs={'class': 'first-img'})
    product_names = soup.find_all('div', attrs={'class': 'product-content'})
    product_prices =  soup.find_all('span', attrs={'class': 'price'})
    product_links = soup.find_all('div', attrs={'class': 'product-content'})

    product_image_only = []
    for product_image in product_images:
        product_image_only.append(product_image.attrs['src'])


    product_name_only = []
    for product_name in product_names:
        product_name_only.append(product_name.h4.a.text.strip())

    product_price_only = []
    for product_price in product_prices:
        product_price_only.append(product_price.text.strip())

    product_link_only = []
    for product_link in product_links:
        product_link_only.append(product_link.h4.a.attrs['href'])

    

    df_img = pd.DataFrame({'image':product_image_only})
    df_name = pd.DataFrame({'name':product_name_only})
    df_price = pd.DataFrame({'price':product_price_only})
    df_link = pd.DataFrame({'link':product_link_only})

    df = pd.concat([df_img,df_name,df_price,df_link], axis=1)
    df['icon'] = 'https://www.computersourcebd.com/asset/view/new/assets/img/logo/logo2.png'

    return df


