import pandas as pd
import pickle
from fastapi import FastAPI
import uvicorn
from client_features import ClientFeatures

with open("trained_pipeline.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()


@app.get('/')
def say_hello():
    return "Hello!"
    
@app.post('/score')
async def give_score(data:ClientFeatures):
    data_dict = data.dict()
    df = pd.DataFrame([data_dict])
    score = model.predict_proba(df)[0][1]
    score = round(score, 2)
    if score < 0.4933:
        status = 'Accepted'
    else:
        status = 'Rejected'

    print(score, status)
    return {"risk_score": score, 
            'application_status': status}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)