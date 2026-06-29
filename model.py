import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler

MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "models"
)

def train_models(df, feature_cols):
    X = df[feature_cols].values
    y = df["placement_status"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    models = {
        "Random Forest":       (RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42), False),
        "Gradient Boosting":   (GradientBoostingClassifier(n_estimators=200, max_depth=4, random_state=42), False),
        "Logistic Regression": (LogisticRegression(max_iter=1000, random_state=42), True),
        "SVM":                 (SVC(probability=True, kernel="rbf", random_state=42), True),
    }

    results = {}
    for name, (model, needs_scale) in models.items():
        Xtr = X_train_scaled if needs_scale else X_train
        Xte = X_test_scaled  if needs_scale else X_test
        model.fit(Xtr, y_train)
        preds = model.predict(Xte)
        proba = model.predict_proba(Xte)[:, 1]
        cv    = cross_val_score(model, Xtr, y_train, cv=5)
        results[name] = {
            "accuracy":         round(accuracy_score(y_test, preds) * 100, 2),
            "auc":              round(roc_auc_score(y_test, proba), 4),
            "cv_mean":          round(cv.mean() * 100, 2),
            "cv_std":           round(cv.std()  * 100, 2),
            "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
            "model":            model,
            "needs_scale":      needs_scale,
        }

    os.makedirs(MODEL_DIR, exist_ok=True)
    best_name = max(results, key=lambda k: results[k]["cv_mean"])
    joblib.dump(results[best_name]["model"],       os.path.join(MODEL_DIR, "best_model.pkl"))
    joblib.dump(scaler,                            os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(feature_cols,                      os.path.join(MODEL_DIR, "features.pkl"))
    joblib.dump(results[best_name]["needs_scale"], os.path.join(MODEL_DIR, "needs_scale.pkl"))

    return results, best_name, X_test, y_test


def load_best_model():
    p = lambda f: os.path.join(MODEL_DIR, f)
    if not os.path.exists(p("best_model.pkl")) or not os.path.exists(p("needs_scale.pkl")):
        return None, None, None, None
    return (
        joblib.load(p("best_model.pkl")),
        joblib.load(p("scaler.pkl")),
        joblib.load(p("features.pkl")),
        joblib.load(p("needs_scale.pkl")),
    )


def predict_placement(model, scaler, features, needs_scale, input_data):
    df_in = pd.DataFrame([input_data], columns=features)
    arr   = scaler.transform(df_in.values) if needs_scale else df_in.values
    proba = model.predict_proba(arr)[0][1]
    return (1 if proba >= 0.5 else 0), round(proba * 100, 2)