from fastapi import FastAPI
import pandas as pd
from ml_logic.registry import load_model
from ml_logic.preprocessor import preprocess_for_inference

app = FastAPI()

@app.get("/")
def route():
    return {"message": "Hello World! Fraud Detection API is running!"}

@app.get("/predict")
def predict(
    Time: float,
    Amount: float,
    V1: float, V2: float, V3: float, V4: float, V5: float, V6: float, V7: float,
    V8: float, V9: float, V10: float, V11: float, V12: float, V13: float,
    V14: float, V15: float, V16: float, V17: float, V18: float, V19: float,
    V20: float, V21: float, V22: float, V23: float, V24: float, V25: float,
    V26: float, V27: float, V28: float
):
    model = load_model()

    X = pd.DataFrame([locals()]) # it will ollect all inputs automatically

    X_processed = preprocess_for_inference(X)
    proba = model.predict_proba(X_processed)[0, 1]

    if proba > 0.5:
        return {"The likelihood of being a Fraud is ": float(proba), "fraud": True}
    else:
        return {"The likelihood of being a Fraud is": float(proba)}

# it ll work locally with:
# uvicorn api.fast:app --reload
