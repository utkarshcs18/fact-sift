"""
clean it, create train / val / test splits, and persist to data/processed/.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
from datasets import load_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
LABEL_MAP = {"SUPPORTS": 0, "REFUTES": 1, "NOT ENOUGH INFO": 2}
LABEL_NAMES = {v: k for k, v in LABEL_MAP.items()}


def _download_fever() -> pd.DataFrame:
    print("[preprocess] Downloading FEVER dataset from HuggingFace …")
    ds = load_dataset("fever", "v1.0", split="paper_dev", trust_remote_code=True)
    df = pd.DataFrame(ds)
    print(f"[preprocess] Downloaded {len(df):,} rows.")
    return df


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    # The FEVER dataset has columns: id, label, claim, evidence_*
    # We only need claim + label for classification training.
    keep_cols = ["claim", "label"]
    available = [c for c in keep_cols if c in df.columns]
    df = df[available].copy()

    # Drop rows with missing claim or label
    df.dropna(subset=available, inplace=True)

    # Normalise label strings → ints
    df["label_id"] = df["label"].map(LABEL_MAP)
    df.dropna(subset=["label_id"], inplace=True)
    df["label_id"] = df["label_id"].astype(int)

    # Drop duplicate claims
    df.drop_duplicates(subset=["claim"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f"[preprocess] After cleaning: {len(df):,} rows.")
    return df


def _split_and_save(df: pd.DataFrame) -> None:
    from sklearn.model_selection import train_test_split

    train_df, temp_df = train_test_split(
        df, test_size=0.30, random_state=42, stratify=df["label_id"]
    )
    val_df, test_df = train_test_split(
        temp_df, test_size=0.50, random_state=42, stratify=temp_df["label_id"]
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for name, split_df in [("train", train_df), ("val", val_df), ("test", test_df)]:
        path = OUTPUT_DIR / f"{name}.csv"
        split_df.to_csv(path, index=False)
        print(f"[preprocess] Saved {name} → {path}  ({len(split_df):,} rows)")


def main() -> None:
    df = _download_fever()
    df = _clean(df)
    _split_and_save(df)
    print("[preprocess] Done ✓")


if __name__ == "__main__":
    main()
