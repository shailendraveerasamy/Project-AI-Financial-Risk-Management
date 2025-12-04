from ml_logic.model import build_model, train, evaluate, cross_validate
# from ml_logic.preprocessor import load_and_preprocess_data

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler


# loading the data
data = pd.read_csv("raw_data/creditcard.csv")
X = data.drop('Class', axis=1)
y = data['Class']

# splitting the data into train and test sets
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
)


# scaling
scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled   = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# the model
model = build_model()

# --- Cross validation ---
scores = cross_validate(model, X_train_scaled, y_train)
print("CV scores:", scores)

# train z model with function imported from ml_logic/model
train(model, X_train_scaled, y_train, X_val_scaled, y_val)

# evaluate the model with imported function from ml_logic/model
result = evaluate(model, X_test_scaled, y_test, threshold=0.5)
print(result["classification_report"])
print(result["confusion_matrix"])
