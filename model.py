import numpy as np
import pickle
import pandas as pd

# Loading the trained model from a saved file
with open("trained_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

# Defining a function to predict the risk score 
#and application status of new data
def get_score(data):
    score = model.predict_proba(data)[0, 1]
    score = round(score,2)
    if score < 0.4966:
        status = 'Accepted'
    else:
        status = 'Rejected'

    return {"risk_score": score, 'application_status': status}
                      