import joblib
from pathlib import Path

MODEL_PATH = Path("models/model.joblib")
MODEL_PATH.parent.mkdir(exist_ok=True, parents=True)

def save_model(model):
    """
    we are saving the trained model to a joblib file/disc
    """
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved at {MODEL_PATH}")

def load_model():
    """
    we are loading previously trained/saved model from joblib file/disc
    """
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    else:
        return ("No model found! Train it first!")
