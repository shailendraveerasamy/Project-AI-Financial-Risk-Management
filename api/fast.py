from fastapi import FastAPI
import pandas as pd
from ml_logic.registry import load_model
# from ml_logic.preprocessor import preprocess_for_inference
from datetime import datetime
from ml_logic.preprocessor import preprocess_new_data

app = FastAPI()

@app.get("/")
def route():
    return {"message": "Hello World! Fraud Detection API is running on the cloud now!"}


@app.get("/predict_new")
def predict_new(
    trans_date_trans_time : str,
    category: str,
    amt: float,
    gender: str,
    lat: float,
    long: float,
    dob: str,
    merch_lat: float,
    merch_long: float
):
    model = load_model()
    #Transform trans_date_trans_time into string which then will be transform in datetime in preprocess
    trans_date_trans_time = str(datetime.strptime(trans_date_trans_time, "%Y-%m-%d %H:%M:%S"))

    #
    X=[trans_date_trans_time, category, amt, gender, lat, long, dob, merch_lat, merch_long]
    columns = ['trans_date_trans_time', 'category', 'amt', 'gender', 'lat', 'long', 'dob', 'merch_lat', 'merch_long']
    X = pd.DataFrame([X], columns=columns)

    X_processed = preprocess_new_data(X)
    proba = model.predict_proba(X_processed)[0, 1]

    if proba > 0.5:
        return {"The likelihood of being a Fraud is ": float(proba), "fraud": True}
    else:
        return {"The likelihood of being a Fraud is": float(proba)}



# # it ll work locally with:
# # uvicorn api.fast:app --reload
