import csv

def state(state_to_filter):
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

    next_empty_row_index = None
    for i, row in enumerate(main_table_data[4:], start=4):
        if len(row) < 20:
            row.extend([''] * (20 - len(row)))
        if row[19] == '':
            next_empty_row_index = i
            break

    if next_empty_row_index is None:
        next_empty_row_index = len(main_table_data)
        new_row = [''] * 20
        main_table_data.append(new_row)

    # Ensure no duplicate entries for the same state
    for row in main_table_data[4:]:
        if row[2] == state_to_filter:
            row[19] = str(dispatch_seats_sum)
            break
    else:
        main_table_data[next_empty_row_index][19] = str(dispatch_seats_sum)

    with open('main_table.csv', mode='w', newline='', encoding='utf-8') as main_file:
        csv_writer = csv.writer(main_file)
        csv_writer.writerows(main_table_data)

    print(f"Total dispatch seats for state {state_to_filter}: {dispatch_seats_sum}")

state('AL')
state('AK')
state('AZ')
state('AR')
state('CO')
state('CT')
state('DE')
state('FL')
state('GA')
state('HI')
state('ID')
state('IL')
state('IN')
state('IA')
state('KS')
state('KY')
state('LA')
state('ME')
state('MD')
state('MA')
state('MI')
state('MN')
state('MO')
state('MT')
state('NE')
state('NV')
state('NH')
state('NJ')
state('NM')
state('NY')
state('NC')
state('ND')
state('TX')
state('CA')
state('OH')
state('OK')
state('OR')
state('PA')
state('RI')
state('SC')
state('SD')
state('TX')
state('CA')
state('TN')
state('UT')
state('VT')
state('VA')
state('WA')
state('WV')
state('WI')
state('WY')