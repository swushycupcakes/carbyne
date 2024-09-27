import pandas as pd
import re
df = pd.read_excel("raw_data/Don Le Territory.xlsx", sheet_name="Bulk Upload Template")

with open('parsed.txt', 'r') as file:
    content = file.read()

lines = content.split('\n')

company_websites = {}

for line in lines:
    match = re.match(r'Website for (.+?): (.+)', line)
    if match:
        company_name = match.group(1).strip()
        website = match.group(2).strip()
        company_websites[company_name] = website


def get_website(row):
    company_name = row['Legal Account Name']
    return company_websites.get(company_name, row['Website'])

df['Website'] = df.apply(get_website, axis=1)

print(df[['Legal Account Name', 'Website']])

df.to_excel("Updated Don Le Territory.xlsx", index=False)