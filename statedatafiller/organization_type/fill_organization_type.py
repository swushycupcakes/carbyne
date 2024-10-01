import pandas as pd

INPUT_PATH = "raw_data/"
OUTPUT_PATH = "processed_data/"



def get_type(account_name):
    split_string = list(map(lambda x: x.lower(), account_name.split(" ")))
    lower_name = account_name.lower()
    
    if split_string[-1] == "county":
        return "Police, University & College"
    if split_string[-1] == "center":
        return "Dispatch Center (Stand Alone)"
    if "police" in lower_name:
        return "Police, Municipal"
    if "sheriff" in lower_name:
        return "County, Sheriff or Police"
    if "county" in lower_name or split_string[-1] == "9-1-1":
        return "Dispatch Center (Stand Alone)"
    if "chp" in lower_name:
        return "County, Sheriff or Police"
    if "park" in lower_name:
        return "County, Sheriff or Police"
    if "city" in lower_name or "regional" in lower_name:
        return "Police, University & College"
    else:
        return "Corporation"
    
def populate_org_type(sheet_df):
    sheet_df["Organization Type"] = sheet_df.apply(lambda row: get_type(row["Account Name"]) if pd.isna(row["Organization Type"]) else row["Organization Type"], axis = 1)
    return sheet_df
    

states = ["CA", "CO", "FL", "GA", "IL", "MO", "NV", "OH", "OK", "PA", "SC", "TX", "VA", "WA"]

raw_data = pd.read_excel(f"{INPUT_PATH}raw_data.xlsx", sheet_name = None)

for sheet_name, sheet_df in raw_data.items():
    if sheet_name in states:
        raw_data[sheet_name] = populate_org_type(sheet_df)

with pd.ExcelWriter('processed_data/processed_excel_file.xlsx') as writer:
    for sheet_name, processed_sheet in raw_data.items():
        processed_sheet.to_excel(writer, sheet_name=sheet_name, index=False)