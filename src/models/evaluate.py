"""
the test split.  Reports accuracy, macro-F1, per-class precision / recall,
and confusion matrices.
"""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
ML_MODEL_PATH = PROJECT_ROOT / "models" / "fact_sift_ml.joblib"
DL_MODEL_DIR = PROJECT_ROOT / "models" / "distilbert_fact_sift"

LABEL_NAMES = ["SUPPORTS", "REFUTES", "NOT ENOUGH INFO"]


def _load_test() -> pd.DataFrame:
    path = DATA_DIR / "test.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python -m src.data.preprocess` first."
        )
    return pd.read_csv(path)


def _print_report(name: str, y_true, y_pred) -> None:
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="macro")
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")
    print(f"  Accuracy : {acc:.4f}")
    print(f"  Macro-F1 : {f1:.4f}\n")
    print(classification_report(y_true, y_pred, target_names=LABEL_NAMES))
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:")
    print(pd.DataFrame(cm, index=LABEL_NAMES, columns=LABEL_NAMES))
    print()


def evaluate_ml(test_df: pd.DataFrame) -> None:
    if not ML_MODEL_PATH.exists():
        print("[evaluate] ML model not found – skipping.")
        return
    pipe = joblib.load(ML_MODEL_PATH)
    y_pred = pipe.predict(test_df["claim"].values)
    _print_report("ML – TF-IDF + Logistic Regression", test_df["label_id"].values, y_pred)


def evaluate_dl(test_df: pd.DataFrame) -> None:
    if not DL_MODEL_DIR.exists():
        print("[evaluate] DL model not found – skipping.")
        return

    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(str(DL_MODEL_DIR))
    model = AutoModelForSequenceClassification.from_pretrained(str(DL_MODEL_DIR))
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    claims = test_df["claim"].tolist()
    preds: list[int] = []
    batch_size = 64

    for i in range(0, len(claims), batch_size):
        batch = claims[i : i + batch_size]
        enc = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt",
        ).to(device)
        with torch.no_grad():
            logits = model(**enc).logits
        preds.extend(logits.argmax(dim=-1).cpu().tolist())

    _print_report(
        "DL – DistilBERT (fine-tuned)",
        test_df["label_id"].values,
        np.array(preds),
    )


def main() -> None:
    test_df = _load_test()
    print(f"[evaluate] Test set: {len(test_df):,} rows.")
    evaluate_ml(test_df)
    evaluate_dl(test_df)
    print("[evaluate] Done ✓")


if __name__ == "__main__":
    main()
