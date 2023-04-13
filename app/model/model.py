#!/usr/bin/env python
# coding: utf-8


import uvicorn
from fastapi import FastAPI
import numpy as np
import pickle
import pandas as pd
from pydantic import BaseModel
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

with open(f"{BASE_DIR}/trained_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

class ClientFeatures(BaseModel):
    NAME_INCOME_TYPE: str
    NAME_EDUCATION_TYPE: str
    DAYS_BIRTH: int
    DAYS_EMPLOYED_PERC: float
    REGION_RATING_CLIENT: int
    EXT_SOURCE_1: float
    EXT_SOURCE_2: float
    EXT_SOURCE_3: float

def give_score(data:ClientFeatures):
    df = pd.DataFrame([data.values()], columns=data.keys())
    score = model.predict_proba(df)[0, 1]
    score = round(score,2)
    print("Test, score is: ", score)
    if score < 0.33:
        status = 'Accepted'
    else:
        status = 'Rejected'

    return {"risk_score": score, 'application_status': status}
                      