from fastapi import FastAPI
import pandas as pd
from ml_logic.registry import load_model
from ml_logic.preprocessor import preprocess_for_inference
from datetime import datetime
from ml_logic.preprocessor import preprocess_new_data

app = FastAPI()

@app.get("/")
def route():
    return {"message": "Hello World! Fraud Detection API is running!"}

@app.get("/predict")
def predict(
    Time: str,
    Amount: float,
    V1: float, V2: float, V3: float, V4: float, V5: float, V6: float, V7: float,
    V8: float, V9: float, V10: float, V11: float, V12: float, V13: float,
    V14: float, V15: float, V16: float, V17: float, V18: float, V19: float,
    V20: float, V21: float, V22: float, V23: float, V24: float, V25: float,
    V26: float, V27: float, V28: float
):
    model = load_model()
    # try except added to solve issues with time after it is changed to str ...
    try:
        Time = pd.to_datetime(Time)
        Time = (Time - pd.Timestamp("1970-01-01")) / pd.Timedelta(seconds=1)
    except Exception:
        return {"error": "Invalid Time format. Use YYYY-MM-DD HH:MM:SS"}
    #
    X = pd.DataFrame([locals()]) # it will ollect all inputs automatically
    X_processed = preprocess_for_inference(X)
    proba = model.predict_proba(X_processed)[0, 1]
    if proba > 0.5:
        return {"The likelihood of being a Fraud is ": float(proba), "fraud": True}
    else:
        return {"The likelihood of being a Fraud is": float(proba)}
# it ll work locally with:
# uvicorn api.fast:app --reload

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

# it ll work locally with:
# uvicorn api.fast:app --reload
