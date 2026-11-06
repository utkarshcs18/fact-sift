"""
classification.  Trains on processed data and saves the pipeline to
models/fact_sift_ml.joblib.
"""

from __future__ import annotations

import os
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "fact_sift_ml.joblib"

LABEL_NAMES = {0: "SUPPORTS", 1: "REFUTES", 2: "NOT ENOUGH INFO"}


def _load_split(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python -m src.data.preprocess` first."
        )
    return pd.read_csv(path)


def build_pipeline() -> Pipeline:
    return Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=50_000,
                    ngram_range=(1, 2),
                    sublinear_tf=True,
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    C=1.0,
                    solver="lbfgs",
                    multi_class="multinomial",
                    n_jobs=-1,
                ),
            ),
        ]
    )


def main() -> None:
    print("[train_ml] Loading processed data …")
    train_df = _load_split("train")
    val_df = _load_split("val")

    X_train, y_train = train_df["claim"].values, train_df["label_id"].values
    X_val, y_val = val_df["claim"].values, val_df["label_id"].values

    pipe = build_pipeline()
    print("[train_ml] Training TF-IDF + Logistic Regression …")
    pipe.fit(X_train, y_train)

    # Evaluate on validation set
    y_pred = pipe.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    print(f"[train_ml] Validation accuracy: {acc:.4f}")
    print(
        classification_report(
            y_val, y_pred, target_names=list(LABEL_NAMES.values())
        )
    )

    # Save
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    print(f"[train_ml] Model saved → {MODEL_PATH}")


if __name__ == "__main__":
    main()
