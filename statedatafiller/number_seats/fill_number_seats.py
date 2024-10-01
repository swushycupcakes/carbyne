import pandas as pd

INPUT_PATH = "raw_data/"
OUTPUT_PATH = "processed_data/"


def populate_seat_nums(sheet_name, sheet_df):
    state_seats_df = seats[seats["State"] == sheet_name]
    state_seats_df = state_seats_df[["Account Name", "Dispatch Seats"]]
    state_seats_df['Account Name'] = f"US {sheet_name} " + state_seats_df['Account Name']
    # print(state_seats_df)
    df_seats_merged = pd.merge(sheet_df, state_seats_df, on='Account Name', how='left')

    return df_seats_merged

    



states = ["CA", "CO", "FL", "GA", "IL", "MO", "NV", "OH", "OK", "PA", "SC", "TX", "VA", "WA"]

raw_data = pd.read_excel(f"{OUTPUT_PATH}org_types_done.xlsx", sheet_name = None)
seats = pd.read_excel(f"{INPUT_PATH}raw_psap_seats.xlsx", sheet_name = "Full List")

for sheet_name, sheet_df in raw_data.items():
    if sheet_name in states:
        raw_data[sheet_name] = populate_seat_nums(sheet_name, sheet_df)

with pd.ExcelWriter('processed_data/seats_excel_file.xlsx') as writer:
    for sheet_name, processed_sheet in raw_data.items():
        processed_sheet.to_excel(writer, sheet_name=sheet_name, index=False)