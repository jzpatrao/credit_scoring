import pandas as pd
import pickle
from fastapi import FastAPI
import uvicorn
from client_features import ClientFeatures
import os
from fastapi.responses import JSONResponse

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

    print(result)
    return JSONResponse(content=result)


# Heroku
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("my_api:app", host='0.0.0.0', port=port, reload=True, root_path="/api")

# Local
# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=8000)