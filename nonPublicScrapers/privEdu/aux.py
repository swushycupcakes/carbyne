def print_column_headers(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        headers = first_line.split(',')
        for header in headers:
            print(header)

# Assuming the file is located at the specified path
print_column_headers('output/public_schools.csv')
