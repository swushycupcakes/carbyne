import csv
import pandas as pd    
import os

def filter_and_save_csv(input_file_path, output_file_path):
    columns_to_keep = ['NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'TELEPHONE', 'COUNTY', 'WEBSITE', 'LEVEL_']

    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        writer = csv.DictWriter(outfile, fieldnames=columns_to_keep)
        writer.writeheader()

        for row in reader:
            filtered_row = {key: row[key] for key in columns_to_keep if key in row}
            writer.writerow(filtered_row)

def convert_csv_to_excel(input_file_path, output_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file_path)

    # Check if 'STATE' column exists
    if 'STATE' in df.columns:
        # Create a Pandas Excel writer using XlsxWriter as the engine
        with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
            # Group the DataFrame by 'STATE' and write each group to a separate sheet
            for state, group in df.groupby('STATE'):
                group.to_excel(writer, sheet_name=state, index=False)
    else:
        print("The 'STATE' column is not present in the CSV file.")


if __name__ == "__main__":
    input_csv_file_path = 'public_schools.csv'
    output_csv_file_path = 'output/public_schools.csv'
    output_excel_file_path = 'output/public_schools_by_state.xlsx'

    if not os.path.exists(output_csv_file_path):
        filter_and_save_csv(input_csv_file_path, output_csv_file_path)
        
    convert_csv_to_excel(output_csv_file_path, output_excel_file_path)

if os.path.exists(output_excel_file_path):
    print(f"File successfully created at {output_excel_file_path}")
else:
    print("File not found. Something went wrong.")
    