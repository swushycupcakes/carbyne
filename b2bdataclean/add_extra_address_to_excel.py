import pandas as pd

"""
Some of the addresses were not parsed initially with web-scraping. These addresses are in address/extra_addresses.csv. Fetch those addresses and put them into the master excel to create a file with both websites and addresses  
"""

df1 = pd.read_excel("processed_data/Addresses.xlsx")

df_extra = pd.read_csv("address/extra_addresses.csv")


df = pd.merge(df1, df_extra[['Legal Account Name', 'Billing Address', "City", "State", "Zip"]], on='Legal Account Name', how='left', suffixes=('', '_df2'))


df['Billing Address'] = df['Billing Address'].fillna(df['Billing Address_df2'])
df['City'] = df['City'].fillna(df['City_df2'])
df['State'] = df['State'].fillna(df['State_df2'])
df['Zip'] = df['Zip'].fillna(df['Zip_df2'])

df = df.drop(["Billing Address_df2", "City_df2", "State_df2", "Zip_df2"], axis = 1)


df.to_excel("processed_data/WebAdd Don Le Territory.xlsx", index=False)