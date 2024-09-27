# Carbyne b2b data cleaning code
This repo contains the code used to clean the b2b Salesforce account data for Carbyne. Specifically, the task was to populate a master excel with the addresses, websites, and counties of accounts.

Each file has a docstring to explain it. 

IMPORTANT: Download a chrome web driver from https://developer.chrome.com/docs/chromedriver/downloads for your version of chrome. Place the unzipped folder in the root folder. I am using the latest version of chrome, but if you are having errors with the web-scraping you most likely need to switch the driver. Contact me (Neel Kondapalli) with questions. 

Here's how it works:

1. Raw excel file is stored in `raw_data/`
2. New files are stored in `processed_data/`
3. `website/scrape_website.py` scrapes website data and populates `website/websites.csv` as it goes. If the scraping times/errors out, the progress is saved within the CSV file. Every time the scraping times out, run `website_csv_to_master_excel.py` to create a new excel with the new websites parsed. This way, the scraper does not start from scratch (you will need to change the hardcoded source excel file in `website/scrape_website.py`)
4. Once you have a excel file that has all the websites in it, move onto addresses.
5. `address/scrape_address.py` uses (initially) the raw excel and does the same thing as the website script. Every time the scraper dies, run `address_csv_to_excel.py` to create a latest Address excel. Change the source in `address/scrape_address.py` to use this latest file. 
6. Some of the addresses could not be parsed by the scraper (due to formatting, etc.). Running `address_excel_to_master_excel.py` creates a updated excel named Concat with all the latest data (it combines the Address and Website excels). Use this excel to find the missing addresses, which are put into `address/extra_addresses.csv`. 
7. Run `add_extra_address_to_excel.py` to create a excel file with all the addresses and all the websites, called WebAdd
8. Finally, counties. The counties are located in `address/counties.csv`. Run `add_counties_to_excel.py` to add this column onto the WebAdd excel, and you have a final excel file.