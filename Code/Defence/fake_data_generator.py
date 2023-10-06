import hashlib
import requests
from faker import Faker
import time

def generate_fake_data():
    fake = Faker()

    # Generate fake data
    fake_data = {
        "data":{
        'eventtype': fake.random_element(elements=('status', 'leave')),
        'epocutc': str(fake.date_time_between(start_date='-60d', end_date='now').timestamp())[:-2],
        'zone': fake.random_element(elements=('bz2454','bz2453','bz2452','bz2457','bz2458')),
        'mac_address': hashlib.sha224(fake.mac_address().encode()).hexdigest(),
        'RSSI': fake.random_int(min=-300, max=0),
        'techtype': fake.random_element(elements=('0','1','2'))
    }}
    return fake_data

for i in range(1,1000):
    data=generate_fake_data()
    print(data)
    # Make request to the '/fake_data' endpoint in app.py
    response = requests.post('http://192.168.30.140:80/postjson', json=data)
    print(response.text)
    time.sleep(2)

