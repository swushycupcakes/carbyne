import csv
import pandas as pd    
import os
import os

# Set working directory to Downloads folder
os.chdir('/Users/chrislee/Downloads')  

# Now you can reference files directly by name
input_csv_file_path = 'us-private-schools.csv'

def filter_and_save_csv(input_file_path, output_file_path):
    # Specify the columns to keep
    columns_to_keep = ['NAME', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'TELEPHONE', 'COUNTY', 'SOURCE']

    # Open input CSV and output CSV files
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=';')  # Adjust delimiter if needed
        writer = csv.DictWriter(outfile, fieldnames=columns_to_keep)
        writer.writeheader()

        # Write only the specified columns to the output CSV
        for row in reader:
            filtered_row = {key: row[key] for key in columns_to_keep if key in row}
            writer.writerow(filtered_row)

def convert_csv_to_excel(input_file_path, output_file_path):
    # Load the CSV data into a DataFrame
    df = pd.read_csv(input_file_path)

    # Check if 'STATE' column exists
    if 'STATE' in df.columns:
        # Create an Excel writer
        with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
            # Group data by 'STATE' and save each group to a separate sheet
            for state, group in df.groupby('STATE'):
                group.to_excel(writer, sheet_name=state, index=False)
    else:
        print("The 'STATE' column is not present in the CSV file.")

if __name__ == "__main__":
    # File paths
    input_csv_file_path = 'us-private-schools.csv'  # Use the uploaded file path
    output_csv_file_path = 'output/filtered_private_schools.csv'
    output_excel_file_path = 'output/private_schools_by_state.xlsx'

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv_file_path), exist_ok=True)

    # Filter columns and save to new CSV
    if not os.path.exists(output_csv_file_path):
        filter_and_save_csv(input_csv_file_path, output_csv_file_path)
        
    # Convert filtered CSV to Excel with separate sheets per state
    convert_csv_to_excel(output_csv_file_path, output_excel_file_path)

    if os.path.exists(output_excel_file_path):
        print(f"File successfully created at {output_excel_file_path}")
    else:
        print("File not found. Something went wrong.")