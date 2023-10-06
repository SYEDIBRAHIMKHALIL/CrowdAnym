import psycopg2
import datetime
import json
import requests
import csv

# Connect to your postgres DB
conn = psycopg2.connect(
    host='141.13.162.170',
    port='5432',
    user='crowdanym_reader',
    password='cranym_read',
    dbname='testdb'
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Start and end timestamps in datetime format
start_timestamp = datetime.datetime(2023, 7, 16, 22, 0, 0)
end_timestamp = datetime.datetime(2023, 7, 30, 21, 59, 59)

# Query
query = f"""
    SELECT * FROM testschemadb.flowtrack_raw
    WHERE epocutc >= '{start_timestamp}' AND epocutc <= '{end_timestamp}'
    ORDER BY epocutc ASC;
"""

# Execute the query
cur.execute(query)

# Fetch all records
rows = cur.fetchall()

# Open CSV file
with open('mac_address_testing.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(['eventtype', 'epocutc', 'zone', 'mac_address', 'RSSI', 'techtype'])

    # Process each row
    for row in rows:
        new_row = list(row)

        # If 'epocutc' is a datetime, convert it to a timestamp
        if isinstance(new_row[1], datetime.datetime):
            new_row[1] = str(new_row[1].timestamp())[:-2]  # Remove the last two characters

        writer.writerow(new_row)

# Close communication
cur.close()
conn.close()