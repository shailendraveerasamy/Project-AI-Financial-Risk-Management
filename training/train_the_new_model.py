from ml_logic.model import build_new_model, train_new_model, evaluate
from ml_logic.registry import save_model
from ml_logic.preprocessor import save_scaler
from ml_logic.preprocessor import preprocess_new_data
from ml_logic.preprocessor import drop_useless_columns

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler


# loading the data
data = pd.read_csv("raw_data/fraudTrain.csv")

X = data.drop('is_fraud', axis=1)
y = data['is_fraud']

X_transformed=drop_useless_columns(X)
X_transformed=preprocess_new_data(X_transformed)

# splitting the data into train and test sets
X_train, X_temp, y_train, y_temp = train_test_split(
    X_transformed, y, test_size=0.3, stratify=y, random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)


# the model
model = build_new_model()

# --- Cross validation --- I put in comment for the moment. SEE LATER how to add categorical_features in training
#scores = cross_validate(model, X_train_scaled, y_train)
#print("CV scores:", scores)

# train z model with function imported from ml_logic/model
train_new_model(model, X_train, y_train, X_val, y_val)

# evaluate the model with imported function from ml_logic/model
result = evaluate(model, X_test, y_test, threshold=0.5)
print(result["classification_report"])
print(result["confusion_matrix"])

# newly added function to save the model so docker/FastAPI can use it, it's saved upon running the command: python training/train_the_model.py
save_model(model)
