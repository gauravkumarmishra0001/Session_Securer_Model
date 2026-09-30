
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.services.feature_engineering_service import (
    ML_FEATURE_NAMES
)


MODEL_PATH = Path(
    "models/isolation_forest.joblib"
)


def train_isolation_forest(
    training_data_path="data/ml_training_data.csv",
    model_path=MODEL_PATH,
    contamination=0.05,
    n_estimators=200,
    random_state=42
):
    df = pd.read_csv(training_data_path)

    missing_features = [
        feature
        for feature in ML_FEATURE_NAMES
        if feature not in df.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    X = df[ML_FEATURE_NAMES].astype(float)

    pipeline = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "model",
            IsolationForest(
                n_estimators=n_estimators,
                contamination=contamination,
                random_state=random_state,
                n_jobs=-1
            )
        )
    ])

    pipeline.fit(X)

    decision_scores = pipeline.decision_function(X)

    metadata = {
        "feature_names": ML_FEATURE_NAMES,
        "training_samples": len(X),
        "algorithm": "IsolationForest",
        "n_estimators": n_estimators,
        "contamination": contamination,
        "score_min": float(np.min(decision_scores)),
        "score_max": float(np.max(decision_scores)),
        "score_p05": float(
            np.percentile(decision_scores, 5)
        ),
        "score_p10": float(
            np.percentile(decision_scores, 10)
        )
    }

    artifact = {
        "pipeline": pipeline,
        "metadata": metadata
    }

    model_path = Path(model_path)
    model_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        artifact,
        model_path
    )

    return artifact


def load_isolation_forest(
    model_path=MODEL_PATH
):
    model_path = Path(model_path)

    if not model_path.exists():
        return None

    return joblib.load(model_path)


def predict_isolation_forest(
    feature_vector,
    model_path=MODEL_PATH
):
    artifact = load_isolation_forest(
        model_path
    )

    if artifact is None:
        raise FileNotFoundError(
            f"Model not found: {model_path}"
        )

    pipeline = artifact["pipeline"]

    X = pd.DataFrame(
        [feature_vector],
        columns=ML_FEATURE_NAMES
    )

    prediction = int(
        pipeline.predict(X)[0]
    )

    decision_score = float(
        pipeline.decision_function(X)[0]
    )

    return {
        "prediction": prediction,
        "decision_score": decision_score
    }
