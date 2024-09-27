from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import csv

import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


website_column_names = [
    ["Legal Account Name", "Address"]
]

try:
    df_address = pd.read_csv("addresses.csv")
except:
    with open('addresses.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(website_column_names)


def create_headless_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)

driver = create_headless_driver()



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

        with open('./addresses.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                target, address
        ])
    except:
        print("Could not parse address for {target}")
        address = ""


    return address



#df = pd.read_excel("../raw_data/Don Le Territory.xlsx", sheet_name="Bulk Upload Template")
"""
Scrape addresses from the raw excel or the one with addresses already populated (assuming address_csv_to_excel.py has been run to create/update an Address excel)
"""
df = pd.read_excel("../processed_data/Address Don Le Territory.xlsx", sheet_name="Sheet1")


print(df.head())


df.apply(lambda row: scrape_address(row["Legal Account Name"]) if pd.isna(row["Billing Address"]) else row["Billing Address"], axis = 1)


driver.quit()
