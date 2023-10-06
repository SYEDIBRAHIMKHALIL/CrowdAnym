import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.feature_extraction import FeatureHasher
from joblib import dump
from sklearn.svm import OneClassSVM
import re

# Function to create features - Feature engineering part
def create_features(df):
    # Encode 'eventtype' and 'zone' as per the given conditions
    df['eventtype_encoded'] = df['eventtype'].apply(lambda s: 1 if s in ['status', 'leave'] else 0)
    df['epocutc_encoded'] = df['epocutc'].apply(lambda x: 1 if str(x).isdigit() and len(str(x)) == 10 else 0)
    df['zone_encoded'] = df['zone'].apply(lambda s: 1 if s in ['bz2452', 'bz2453', 'bz2454', 'bz2457', 'bz2458'] else 0)

    df['length'] = df['mac_address'].apply(len)
    df['num_special_chars'] = df['mac_address'].apply(lambda s: sum(not c.isalnum() for c in s))
    df['is_valid_hash'] = df['mac_address'].apply(lambda s: 1 if re.match("^[a-f0-9]{56}$", s) else 0)

    df['RSSI_encoded'] = df['RSSI'].apply(lambda x: 1 if (isinstance(x, int) or isinstance(x, float)) and x >-200 else 0)
    df['techtype_encoded'] = df['techtype'].apply(lambda x: 1 if x in [0, 1, 2] else 0)

    return df

# Read data
df = pd.read_csv('dataset15.csv', error_bad_lines=False)

# Shuffle data and reset index, dropping the old index
df = df.sample(frac=1, random_state=42)

# Drop rows with missing 'mac_address'
df = df.dropna(subset=['mac_address', 'eventtype', 'zone'])

##########
# Splitting dataset into training and testing sets
train_df = df
test_df = pd.read_csv('half_dataset_2.csv', error_bad_lines=False)

# Reset indices
train_df = train_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)

# Drop rows with missing 'mac_address' in test dataset
test_df = test_df.dropna(subset=['mac_address', 'eventtype', 'zone'])

# Apply the function to your dataframes
train_df = create_features(train_df)
test_df = create_features(test_df)

print(train_df)
print("**************************")
print(test_df)
#############
# Drop the original 'mac_address', 'eventtype', 'zone', 'epocutc', 'RSSI', and 'techtype' columns
train_df.drop(columns=['mac_address', 'eventtype', 'zone', 'epocutc', 'RSSI', 'techtype'], inplace=True)
test_df.drop(columns=['mac_address', 'eventtype', 'zone', 'epocutc', 'RSSI', 'techtype'], inplace=True)

# Convert all column names to string
#train_df.columns = train_df.columns.astype(str)
#test_df.columns = test_df.columns.astype(str)
#######
from sklearn.neighbors import LocalOutlierFactor

# Training Isolation Forest
clf = IsolationForest(contamination=0.5)  # contamination factor can be tuned
clf.fit(train_df)
dump(clf, 'isolation_forest.joblib')
##########
# Predict the anomalies in the test data
pred = clf.predict(test_df)

# The model will output -1 for anomalies/outliers and 1 for inliers.
test_df['anomaly'] = pred

############
# Print the anomaly detected data
print(test_df[test_df['anomaly']==-1])
print(len(test_df[test_df['anomaly']==-1]))

print("We have finished!")

# Calculate "accuracy"
accuracy = len(test_df[test_df['anomaly']==-1]) / len(test_df)
print(f"Accuracy: {accuracy}")

##########
from flask import request
from joblib import load
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import numpy as np
from joblib import dump
import re  # don't forget to import the 're' module

# Function to create features - Feature engineering part
def create_features(df):
    # Encode 'eventtype' and 'zone' as per the given conditions
    df['eventtype_encoded'] = df['eventtype'].apply(lambda s: 1 if s in ['status', 'leave'] else 0)
    df['epocutc_encoded'] = df['epocutc'].apply(lambda x: 1 if str(x).isdigit() and len(str(x)) == 10 else 0)
    df['zone_encoded'] = df['zone'].apply(lambda s: 1 if s in ['bz2452', 'bz2453', 'bz2454', 'bz2457', 'bz2458'] else 0)

    df['length'] = df['mac_address'].apply(len)
    df['num_special_chars'] = df['mac_address'].apply(lambda s: sum(not c.isalnum() for c in s))
    df['is_valid_hash'] = df['mac_address'].apply(lambda s: 1 if re.match("^[a-f0-9]{56}$", s) else 0)

    df['RSSI_encoded'] = df['RSSI'].apply(lambda x: 1 if (isinstance(x, int) or isinstance(x, float)) and x > -200 else 0)
    df['techtype_encoded'] = df['techtype'].apply(lambda x: 1 if x in [0, 1, 2] else 0)

    return df

def anomaly_detection(data):
    # Load the models
    clf = load('isolation_forest.joblib')


    # Create a DataFrame from the input data
    df = pd.DataFrame([data])

    # Apply the function to your dataframes
    df = create_features(df)

    # Drop the original 'mac_address' column
    df.drop(columns=['mac_address', 'eventtype', 'zone', 'epocutc', 'RSSI', 'techtype'], inplace=True)

    pred = clf.predict(df)

    # The model will output -1 for anomalies/outliers and 1 for inliers.
    df['anomaly'] = pred

    # Check for anomaly
    if df['anomaly'].values[0] == -1:
        return "The request is malign"
    else:
        return "The request is benign"


data = {
    "eventtype": 'leave',
    "epocutc": '1687014878',
    "zone": 'bz2454',
    "mac_address": '7a92708b92769f9b20029e0ceaf789d8b12dd54b2ff283efd1de4746',
    "RSSI": -180,
    "techtype": 2
}

result = anomaly_detection(data)
print(result)