import pandas as pd

"""
Take the 'County' column from the counties.csv file and add it to the WebAdd excel (which should have both websites and addresses, including missing ones)

"""

df1 = pd.read_excel("processed_data/WebAdd Don Le Territory.xlsx")

df_counties = pd.read_csv("address/counties.csv", usecols = ["County"])


df1["County"] = df_counties["County"]
df1.to_excel("processed_data/Final Don Le Territory.xlsx", index=False)
