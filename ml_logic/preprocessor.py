import joblib
import pandas as pd
from pathlib import Path

# Where the scaler will be saved/loaded
SCALER_PATH = Path("models/scaler.joblib")
SCALER_PATH.parent.mkdir(parents=True, exist_ok=True)


# Save the scaler during training
def save_scaler(scaler):
    """
    Save the fitted scaler (e.g., RobustScaler) to disk.
    """
    joblib.dump(scaler, SCALER_PATH)
    print(f"✅ Scaler saved at {SCALER_PATH}")


# Load the scaler for inference
def load_scaler():
    """
    Load a previously saved scaler.
    """
    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            "Scaler not found. Train the model first (so the scaler is saved)."
        )
    return joblib.load(SCALER_PATH)


# Preprocess incoming inference data
def preprocess_for_inference(X: pd.DataFrame):
    """
    Apply the SAME preprocessing used during training.
    In this project, scaling is the main preprocessing step.
    """
    scaler = load_scaler()

    # Ensure columns are in correct order
    # (VERY IMPORTANT! Must match training order)
    expected_cols = scaler.feature_names_in_

    # Reorder / select the necessary columns
    X = X[expected_cols]

    # Transform using saved scaler
    X_scaled = scaler.transform(X)

    return X_scaled
