from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import csv

import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


website_column_names = [
    ["Legal Account Name", "Website"]
]

df_wesbites = pd.read_csv("websites.csv")
if df_wesbites.empty:
    with open('websites.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(website_column_names)


def create_headless_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)

driver = create_headless_driver()



def scrape_website(target):
    time.sleep(1)
    driver.get('http://www.google.com/')
    search_box = driver.find_element('name', 'q')
    search_box.send_keys(f'{target} company Official Website')
    search_box.submit()
    time.sleep(2)
    
    try:
        element = driver.find_element(By.CSS_SELECTOR, '#search .g .yuRUbf a')
        website =  element.get_attribute("href")
        print(f"Website for {target}: {website}")

        with open('websites.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                target, website
            ])

    except:
        print("Could not parse website for {website}")
        website = ""
 

    return website

def scrape_address(target):
    time.sleep(1)
    driver.get('http://www.google.com/')
    search_box = driver.find_element('name', 'q')
    search_box.send_keys(f'{target} address')
    search_box.submit()
    time.sleep(1)
    try:
        address_element = driver.find_element(By.CSS_SELECTOR, "div.zloOqf span.LrzXr")
        address = address_element.text
        print(f"Website for {target}: {address}")
    except:
        print("Could not parse address for {target}")
        address = ""

    

    return address



#df = pd.read_excel("raw_data/Don Le Territory.xlsx", sheet_name="Bulk Upload Template")
df = pd.read_excel("processed_data/Website Don Le Territory.xlsx", sheet_name="Sheet1")


print(df.head())


df["Website"] = df.apply(lambda row: scrape_website(row["Legal Account Name"]) if pd.isna(row["Website"]) else row["Website"], axis = 1)


print(df["Website"])


target = "Bayer"
#scrape_website(target)

#scrape_address(target)
print("Hello World")
driver.quit()
