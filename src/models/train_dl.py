"""
Saves the model to models/distilbert_fact_sift/ using HuggingFace Trainer.
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "models" / "distilbert_fact_sift"

MODEL_NAME = "distilbert-base-uncased"
NUM_LABELS = 3
LABEL_NAMES = {0: "SUPPORTS", 1: "REFUTES", 2: "NOT ENOUGH INFO"}


def _load_split(name: str) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run `python -m src.data.preprocess` first."
        )
    return pd.read_csv(path)


def _tokenize(examples, tokenizer):
    return tokenizer(
        examples["claim"],
        padding="max_length",
        truncation=True,
        max_length=128,
    )


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average="macro")
    return {"accuracy": acc, "macro_f1": f1}


def main() -> None:
    print("[train_dl] Loading processed data …")
    train_df = _load_split("train")
    val_df = _load_split("val")

    # Convert to HuggingFace Dataset
    train_ds = Dataset.from_pandas(
        train_df[["claim", "label_id"]].rename(columns={"label_id": "label"})
    )
    val_ds = Dataset.from_pandas(
        val_df[["claim", "label_id"]].rename(columns={"label_id": "label"})
    )

    print(f"[train_dl] Tokenising with {MODEL_NAME} …")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    train_ds = train_ds.map(
        lambda ex: _tokenize(ex, tokenizer), batched=True
    )
    val_ds = val_ds.map(lambda ex: _tokenize(ex, tokenizer), batched=True)

    train_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    val_ds.set_format("torch", columns=["input_ids", "attention_mask", "label"])

    print("[train_dl] Loading DistilBERT model …")
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=NUM_LABELS
    )

    training_args = TrainingArguments(
        output_dir=str(OUTPUT_DIR),
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=64,
        num_train_epochs=3,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="macro_f1",
        logging_steps=50,
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    print("[train_dl] Starting fine-tuning …")
    trainer.train()

    # Save best model
    trainer.save_model(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))
    print(f"[train_dl] Model saved → {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
