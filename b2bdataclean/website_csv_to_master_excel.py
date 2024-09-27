import pandas as pd
import csv

"""
Take the websites from website/websites.csv and put them into a Wesbite master excel
"""

df = pd.read_excel("raw_data/Don Le Territory.xlsx", sheet_name="Bulk Upload Template")

df_websites = pd.read_csv("website/websites.csv")




df["Website"] = df_websites["Website"]

df.to_excel("processed_data/Website Don Le Territory.xlsx", index=False)