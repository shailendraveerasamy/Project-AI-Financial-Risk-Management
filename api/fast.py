from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from ml_logic.registry import load_model
# from ml_logic.preprocessor import preprocess_for_inference
from datetime import datetime
from ml_logic.preprocessor import preprocess_new_data

app = FastAPI()

# this is just a middleware in case we need to use other frontend platforms in case we would have issues with streamlit ...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # OK for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def route():
    return {"message": "Hello World! Fraud Detection API is running on the cloud now!"}

model = load_model()
THRESHOLD = 0.5

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
    X = pd.DataFrame([{
        "trans_date_trans_time": trans_date_trans_time,
        "category": category,
        "amt": amt,
        "gender": gender,
        "lat": lat,
        "long": long,
        "dob": dob,
        "merch_lat": merch_lat,
        "merch_long": merch_long
    }])
    # model = load_model()
    #Transform trans_date_trans_time into string which then will be transform in datetime in preprocess
    # trans_date_trans_time = str(datetime.strptime(trans_date_trans_time, "%Y-%m-%d %H:%M:%S"))

    #
    # X=[trans_date_trans_time, category, amt, gender, lat, long, dob, merch_lat, merch_long]
    # columns = ['trans_date_trans_time', 'category', 'amt', 'gender', 'lat', 'long', 'dob', 'merch_lat', 'merch_long']
    # X = pd.DataFrame([X], columns=columns)

    # X_processed = preprocess_new_data(X)
    try:
        X_processed = preprocess_new_data(X)
    except Exception as e:
        return {"error": str(e)}

    proba = model.predict_proba(X_processed)[0, 1]

    return {
        "fraud_probability": float(proba),
        "fraud": bool(proba >= THRESHOLD)
    }


# # it ll work locally with:
# # uvicorn api.fast:app --reload
