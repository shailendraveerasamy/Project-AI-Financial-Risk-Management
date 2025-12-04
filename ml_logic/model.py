from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_score
import xgboost as xgb


BEST_PARAMETERS = {
    'subsample': 1.0,
    'scale_pos_weight': 200,
    'n_estimators': 300,
    'min_child_weight': 3,
    'max_depth': 3,
    'learning_rate': 0.01,
    'gamma': 0.5,
    'colsample_bytree': 0.6
}

def build_model():
    """
    creating an XGBoost model with best parameters retrived via GridSearch() ...
    """
    model = xgb.XGBClassifier(
        **BEST_PARAMETERS,
        random_state=42,
        eval_metric='logloss',
        use_label_encoder=False
    )

    return model

def train(model, X_train, y_train, X_val = None, y_val=None):
    """
    train the model, lets us see if we add validation set
    """
    if X_val is not None:
        model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )
    else:
        model.fit(X_train, y_train)

    return model

def cross_validate(model, X_train, y_train):
    """
    we will perform 5-fold cross validation and stratifiedKFold to avoid overfitting
    """
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring= "average_precision",
        n_jobs=-1
    )

    return scores

def evaluate(model, X_test, y_test, threshold=0.5):
    """
    evaluate the model on the test set using classification metrics ...
    """
    y_proba = model.predict_proba(X_test)[:,1] # on fraud values
    y_pred = (y_proba >= threshold).astype(int)

    report = classification_report(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    conf_metrics = confusion_matrix(y_test, y_pred)

    return {
        "classification_report": report,
        "accuracy": accuracy,
        "confusion_matrix": conf_metrics
    }
