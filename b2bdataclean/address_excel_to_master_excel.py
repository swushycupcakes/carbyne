import pandas as pd

"""
This file added the (incomplete) addresses in Address excel to the existing (complete) website excel to create an intermediary excel with incomplete addresses. This Concat file is used to find missing addresses manually.
These missing addresses are placed into address/extra_addresses.csv
"""

df1 = pd.read_excel("processed_data/Websites.xlsx")

df2 = pd.read_excel("processed_data/Address Don Le Territory.xlsx")

df1["Billing Address"] = df2["Billing Address"]
df1["City"] = df2["City"]
df1["State"] = df2["State"]
df1["Zip"] = df2["Zip"]

df1.to_excel("processed_data/Concat Don Le Territory.xlsx", index=False)