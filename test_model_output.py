import numpy as np
import pandas as pd
import pickle

# Loading the trained model from a saved file
with open("trained_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

# Defining a function to predict the risk score 
#and application status of new data
def get_score(data):
    score = model.predict_proba(data)[0, 1]
    score = round(score, 2)
    if score < 0.4933:
        status = 'Accepted'
    else:
        status = 'Rejected'

    return {"risk_score": score, 'application_status': status}

# Sample data
client_id = 100001
score = 0.38
status = 'Accepted'
data = {'NAME_INCOME_TYPE': ['Working'],
        'DAYS_BIRTH': [-19241],
        'DAYS_EMPLOYED_PERC': [0.121044],
        'REGION_RATING_CLIENT': [2],
        'DAYS_CREDIT': [-857.0],
        'EXT_SOURCE_1': [0.752614],
        'EXT_SOURCE_2': [0.789654],
        'EXT_SOURCE_3': [0.15952]}

# Converting sample data to a pandas DataFrame
sample_df = pd.DataFrame(data)

# Adding the client ID as the first column
sample_df.insert(0, 'SK_ID_CURR', client_id)

# Converting DataFrame to numpy array
sample_data = sample_df.to_numpy()

# Getting the risk score and application status
result = get_score(sample_data)

# Checking the result
assert result['risk_score'] == score
assert result['application_status'] == status
