import psycopg2
import datetime
import json
import requests
import csv
import os

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

# Specify start and end timestamps
start_timestamp = datetime.datetime(2023, 7, 16, 22, 0, 0).timestamp()
end_timestamp = datetime.datetime(2023, 7, 30, 21, 59, 59).timestamp()

# Query
query = f"""
    SELECT * FROM testschemadb.flowtrack_raw
    WHERE epocutc >= to_timestamp({start_timestamp}) AND epocutc <= to_timestamp({end_timestamp})
    ORDER BY epocutc ASC;
"""
# Execute the query
cur.execute(query)

# Fetch all records
rows = cur.fetchall()

# Zones
zones = ["bz2452", "bz2453", "bz2454", "bz2457", "bz2458"]

# Open CSV files for each zone
csv_files = {zone: open(f'D:/UBamberg/{zone}_rate_limit.csv', 'w', newline='') for zone in zones}

# Create CSV writers for each zone
csv_writers = {zone: csv.writer(csv_file) for zone, csv_file in csv_files.items()}

# Write headers to each CSV file
for writer in csv_writers.values():
    writer.writerow(["eventtype", "epocutc", "zone", "mac_address", "RSSI", "techtype"])

# Process rows
for row in rows:
    # Convert the row to a list
    new_row = list(row)

    # Prepare the data in the desired format
    data = {
        'eventtype': new_row[0],
        'epocutc': str(new_row[1].timestamp()),
        'zone': new_row[2],
        'mac_address': new_row[3],
        'RSSI': new_row[4],
        'techtype': new_row[5]
    }

    # Write data to the appropriate CSV file
    if data['zone'] in zones:
        csv_writers[data['zone']].writerow(data.values())

# Close CSV files
for file in csv_files.values():
    file.close()

# Close communication
cur.close()
conn.close()