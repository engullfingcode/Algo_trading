import csv

# Open the CSV file for reading and a new text file for writing
with open('SBIN.csv', 'r') as csv_file, open('SQL_SBIN.txt', 'w') as txt_file:
    csv_reader = csv.reader(csv_file)

    i = 0

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Extract the values from the row
        if i > 2251:
            date = row[0]
            open_price = round((float(row[1]) / 10),4)
            high_price = round((float(row[2]) / 10),4)
            low_price = round((float(row[3]) / 10),4)
            close_price = round((float(row[4]) / 10),4)
            volume = row[5]
        else:
            date = row[0]
            open_price = row[1]
            high_price = row[2]
            low_price = row[3]
            close_price = row[4]
            volume = row[5]


        # Format the values into the desired format
        formatted_row = f"('{date}',{open_price},{high_price},{low_price},{close_price},{volume}),\n"

        # Write the formatted row to the text file
        txt_file.write(formatted_row)
        i = i + 1
