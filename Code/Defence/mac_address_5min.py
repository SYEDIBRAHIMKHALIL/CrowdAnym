import pandas as pd
from datetime import datetime

# Read dataset
df = pd.read_csv('D:/ /mac_address_testing.csv')

# Convert 'epocutc' to datetime format
df['epocutc'] = pd.to_datetime(df['epocutc'], unit='s')

# Create new columns for month, day, hour, and minute
df['month'] = df['epocutc'].dt.month
df['day'] = df['epocutc'].dt.day
df['hour'] = df['epocutc'].dt.hour
df['minute'] = df['epocutc'].dt.minute

# Mapping for minutes
minute_mapping = {
    range(0, 5): 1, range(5, 10): 2, range(10, 15): 3, range(15, 20): 4,
    range(20, 25): 5, range(25, 30): 6, range(30, 35): 7, range(35, 40): 8,
    range(40, 45): 9, range(45, 50): 10, range(50, 55): 11, range(55, 60): 12
}

# Assign the new minute values based on the mapping
for r, new_val in minute_mapping.items():
    df.loc[df['minute'].isin(r), 'minute'] = new_val

# Group by year, month, day, hour, and minute, and get the MAC address that appears the most
df_grouped = df.groupby(['month', 'day', 'hour', 'minute'])['mac_address'].apply(lambda x: x.value_counts().idxmax()).reset_index()

# Count the max occurrence of the MAC address in each group
df_grouped['count'] = df.groupby(['month', 'day', 'hour', 'minute'])['mac_address'].apply(lambda x: x.value_counts().max()).values

# Keep only the columns of interest
df_grouped = df_grouped[['month', 'day', 'hour', 'minute', 'count']]

# Write to a new CSV file
df_grouped.to_csv('D:/UBamberg/mac_each_5min_test.csv', index=False)