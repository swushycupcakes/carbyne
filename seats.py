import csv
state_to_filter = "AL"

dispatch_seats_sum = 0

with open('raw_data.csv', mode='r', newline='', encoding='utf-8') as raw_file:
    csv_reader = csv.reader(raw_file)
    header = next(csv_reader)

    state_index = header.index("State")
    dispatch_seats_index = header.index(" Dispatch Seats ")
    for row in csv_reader:
        if row[state_index] == state_to_filter:
            try:
                dispatch_seats_sum += float(row[dispatch_seats_index])
            except ValueError:
                pass

with open('main_table.csv', mode='r', newline='', encoding='utf-8') as main_file:
    csv_reader = csv.reader(main_file)
    main_table_data = list(csv_reader)

if len(main_table_data) > 4:
    if len(main_table_data[4]) < 20:
        main_table_data[4].extend([''] * (20 - len(main_table_data[4])))
    main_table_data[4][19] = str(dispatch_seats_sum)

with open('main_table.csv', mode='w', newline='', encoding='utf-8') as main_file:
    csv_writer = csv.writer(main_file)
    csv_writer.writerows(main_table_data)

print(f"Total dispatch seats for state {state_to_filter}: {dispatch_seats_sum}")