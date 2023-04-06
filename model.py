import numpy as np
import pickle
import pandas as pd
from pydantic import BaseModel
class ClientFeatures(BaseModel):
    NAME_INCOME_TYPE: str
    NAME_EDUCATION_TYPE: str
    DAYS_BIRTH: int
    DAYS_EMPLOYED_PERC: float
    REGION_RATING_CLIENT: int
    EXT_SOURCE_1: float
    EXT_SOURCE_2: float
    EXT_SOURCE_3: float
        
with open("trained_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

def get_score(data:ClientFeatures):
    print('TEST SCORE data is :', data)
    data = data.dict()
    df = pd.DataFrame([data.values()], columns=data.keys())
    score = model.predict_proba(df)[0, 1]
    score = round(score,2)
    if score < 0.33:
        status = 'Accepted'
    else:
        status = 'Rejected'

    return {"risk_score": score, 'application_status': status}
                      