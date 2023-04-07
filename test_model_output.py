import numpy as np
import pandas as pd
import pytest
import pickle

from model import get_score

def test_get_score():
    # Define sample data
    data = pd.DataFrame({
        'NAME_INCOME_TYPE': ['Working'],
        'NAME_EDUCATION_TYPE': ['Higher education'],
        'DAYS_BIRTH': [-19241],
        'DAYS_EMPLOYED': [-2329],
        'REGION_RATING_CLIENT': [2],
        'EXT_SOURCE_1': [0.752614],
        'EXT_SOURCE_2': [0.789654],
        'EXT_SOURCE_3': [0.15952],
        'DAYS_EMPLOYED_PERC': [0.12]
    })

    # Load the model
    with open("trained_pipeline.pkl", "rb") as f:
        model = pickle.load(f)

    # Calculate the score and status
    result = get_score(data)

    # Check the output
    assert isinstance(result, dict) # Test result type
    assert "risk_score" in result
    assert "application_status" in result
    assert isinstance(result["risk_score"], float) # Test result type
    assert isinstance(result["application_status"], str) # Test result type
