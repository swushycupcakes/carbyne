import pandas as pd

"""
After web-scraping is finished/interrupted, address/addresses.csv contains addresses. Create a Address excel with just those addresses. Keep in mind some accounts may have missing addresses, this will be handled in add_extra_addresses_to_excel.py
"""

df = pd.read_excel("raw_data/Don Le Territory.xlsx", sheet_name="Bulk Upload Template")
df_addresses = pd.read_csv("address/addresses.csv")
df_addresses = df_addresses.drop_duplicates()

df_addresses[['Billing Address', 'City', 'State', 'Zip']] = df_addresses['Address'].str.extract(r'(.+),\s*(.+),\s*([A-Z]{2})\s*(\d{5})')


df = pd.merge(df, df_addresses[['Legal Account Name', 'Billing Address', "City", "State", "Zip"]], on='Legal Account Name', how='left', suffixes=('', '_df2'))

df['Billing Address'] = df['Billing Address'].fillna(df['Billing Address_df2'])
df['City'] = df['City'].fillna(df['City_df2'])
df['State'] = df['State'].fillna(df['State_df2'])
df['Zip'] = df['Zip'].fillna(df['Zip_df2'])

df = df.drop(["Billing Address_df2", "City_df2", "State_df2", "Zip_df2"], axis = 1)


df.to_excel("processed_data/Address Don Le Territory.xlsx", index=False)