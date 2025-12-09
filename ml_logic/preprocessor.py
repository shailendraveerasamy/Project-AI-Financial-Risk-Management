import joblib
import pandas as pd
from pathlib import Path
import numpy as np
# Where the scaler will be saved/loaded
SCALER_PATH = Path("models/scaler.joblib")
SCALER_PATH.parent.mkdir(parents=True, exist_ok=True)


# # Save the scaler during training
def save_scaler(scaler):
    """
    Save the fitted scaler (e.g., RobustScaler) to disk.
    """
    joblib.dump(scaler, SCALER_PATH)
    print(f"✅ Scaler saved at {SCALER_PATH}")


# # Load the scaler for inference
# def load_scaler():
#     """
#     Load a previously saved scaler.
#     """
#     if not SCALER_PATH.exists():
#         raise FileNotFoundError(
#             "Scaler not found. Train the model first (so the scaler is saved)."
#         )
#     return joblib.load(SCALER_PATH)


# # Preprocess incoming inference data
# def preprocess_for_inference(X: pd.DataFrame):
#     """
#     Apply the SAME preprocessing used during training.
#     In this project, scaling is the main preprocessing step.
#     """
#     scaler = load_scaler()

#     # Ensure columns are in correct order
#     # (VERY IMPORTANT! Must match training order)
#     expected_cols = scaler.feature_names_in_

#     # Reorder / select the necessary columns
#     X = X[expected_cols]

#     # Transform using saved scaler
#     X_scaled = scaler.transform(X)

#     return X_scaled

#########################################################################


def preprocess_new_data(X: pd.DataFrame):
    """
    Apply the SAME preprocessing used during training.
    In this project, scaling is the main preprocessing step.
    """
    X = X.copy()   # what isadded
    # X['dob'] = pd.to_datetime(X['dob'])
    if 'dob' in X.columns:
        X['dob'] = pd.to_datetime(X['dob']) # what is changed ...
    X['trans_date_trans_time'] = pd.to_datetime(X['trans_date_trans_time'])
    X['age'] = (X['trans_date_trans_time'] - X['dob']).dt.days / 365.25
    X['trans_month']=pd.to_datetime(X['trans_date_trans_time']).dt.month
    X['trans_day']=pd.to_datetime(X['trans_date_trans_time']).dt.day
    X['trans_hour']=pd.to_datetime(X['trans_date_trans_time']).dt.hour
    X.drop(columns=['trans_date_trans_time','dob'],inplace=True)
    X["trans_month_sin"] = np.sin(2 * np.pi * X["trans_month"] / 12)
    X["trans_month_cos"] = np.cos(2 * np.pi * X["trans_month"] / 12)
    X["trans_day_sin"] = np.sin(2 * np.pi * X["trans_day"] / 31)
    X["trans_day_cos"] = np.cos(2 * np.pi * X["trans_day"] / 31)
    X["trans_hour_sin"] = np.sin(2 * np.pi * X["trans_hour"] / 24)
    X["trans_hour_cos"] = np.cos(2 * np.pi * X["trans_hour"] / 24)
    X.drop(columns=['trans_month','trans_day','trans_hour'],inplace=True)

    return X

def drop_useless_columns(X: pd.DataFrame):
    """
    Drop useless columns
    """
    X.drop(columns=['Unnamed: 0','unix_time','cc_num','first', 'last', 'street', 'city', 'state', 'zip', 'city_pop', 'trans_num'],inplace=True)
    X.drop(columns=['job','merchant'],inplace=True)

    return X
