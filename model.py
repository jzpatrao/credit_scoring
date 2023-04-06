import numpy as np
import pickle
import pandas as pd

with open("trained_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

def get_score(data):

    score = model.predict_proba(data)[0, 1]
    score = round(score,2)
    if score < 0.33:
        status = 'Accepted'
    else:
        status = 'Rejected'

    return {"risk_score": score, 'application_status': status}
                      