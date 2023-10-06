import psycopg2
import datetime
import json
import requests  # new import for sending HTTP requests

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

# Counter
counter = 0

while True:
    # Wait for enter press
    user_input = input("Press Enter to display the next entry or type 'finish' to exit: ")

    if user_input.lower() == 'finish':
        break

    # Query
    query = f"SELECT * FROM testschemadb.flowtrack_raw OFFSET {counter} LIMIT 1"

    # Execute the query
    cur.execute(query)

    # Fetch record
    row = cur.fetchone()

    if row is None:
        break

    new_row = list(row)
    if isinstance(new_row[1], datetime.datetime):
        timestamp = str(new_row[1].timestamp())
        new_row[1] = timestamp[:-2]  # Remove the last two characters

    # Prepare the data in the desired JSON format
    data = {
        'data': {
            'eventtype': new_row[0],
            'epocutc': new_row[1],
            'zone': new_row[2],
            'mac_address': new_row[3],
            'RSSI': new_row[4],
            'techtype': new_row[5]
        }
    }

    print(json.dumps(data, indent=2))  # Display the JSON data

    # Display the type of each item
    #for key, value in data['data'].items():
     #   print(f"The type of '{key}' is {type(value)}")

    # Send the data to the server
    response = requests.post('http://192.168.30.140:80/postjson', json=data)

    print(response.text)  # Display the server's response

    # Increment counter
    counter += 1

# Close communication
cur.close()
conn.close()