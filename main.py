import pandas as pd

df = pd.read_csv('bru.csv')

def fill_organization_type(account_name):
    if 'Police Department' in account_name:
        return 'Police, Municipal'
    elif 'Sherrif' in account_name:
        return 'County, Sheriff or Police'
    else:
        return ''
    
df['Organization Type'] = df['Account Name'].apply(fill_organization_type)

df.to_csv('bru.csv', index=False)