# Fact-Shift

**An evidence-based claim verification system built with classical ML and deep learning.**

Fact-Shift takes a factual claim (a headline, a social media post, a sentence), retrieves evidence, and returns a report: a verdict, the supporting or contradicting passages, source links, and an honest statement of uncertainty. If the evidence is missing or conflicting, it says **NOT ENOUGH EVIDENCE** instead of guessing.

> **Status:** 🚧 In development. See the [Roadmap](#roadmap) for what is done and what is next.

---

## Why this project

A classifier that only reads the wording of a claim cannot know whether the claim is true. Fact-Shift separates two problems:

1. **Claim classification** – what does a trained model predict from the text alone? (baseline)
2. **Evidence-based verification** – does retrieved evidence support or refute the claim? (the real system)

The project compares both approaches with measured results.

## Features (planned)

- Claim input through a web UI and a REST API
- ML baseline: TF-IDF + Logistic Regression
- DL model: fine-tuned DistilBERT / BERT
- Evidence retrieval with semantic ranking of passages
- Natural Language Inference (NLI) to judge SUPPORTS / REFUTES / NOT ENOUGH INFO
- Report with verdict, confidence, source URL and exact passage
- Analysis history stored in PostgreSQL
- Docker setup for reproducible deployment

## Architecture

```
React UI  ──►  FastAPI backend  ──►  Evidence retrieval ──►  Verification model
                    │                                              │
                    ▼                                              ▼
               PostgreSQL                                  Report (verdict + evidence)
          (history, sources, model versions)
```

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Data | Pandas, NumPy |
| ML | scikit-learn |
| DL | PyTorch, Hugging Face Transformers |
| API | FastAPI |
| Frontend | React + Tailwind CSS |
| Database | PostgreSQL |
| Deployment | Docker |

## Dataset

**FEVER** (Fact Extraction and VERification) is the primary dataset: about 185k claims labelled `SUPPORTS`, `REFUTES` or `NOT ENOUGH INFO`, with Wikipedia evidence annotations.

- Official page: https://fever.ai
- Available through Hugging Face `datasets`

Raw data is **not** committed to this repository. Run the download script (see below).

## Project structure

```
fact-shift/
├── data/
│   ├── raw/                # not tracked by git
│   └── processed/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_ml_baseline.ipynb
│   └── 03_dl_experiments.ipynb
├── src/
│   ├── data/preprocess.py
│   ├── models/
│   │   ├── train_ml.py
│   │   ├── train_dl.py
│   │   └── evaluate.py
│   └── verification/
│       ├── retrieve.py
│       └── verify.py
├── backend/
│   ├── main.py
│   ├── schemas.py
│   └── services.py
├── frontend/
├── tests/
├── models/                 # saved models, not tracked by git
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

## Getting started

### 1. Clone and set up the environment

```bash
git clone https://github.com/<your-username>/fact-shift.git
cd fact-shift

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

`requirements.txt` (starting point):

```
pandas
numpy
scikit-learn
joblib
datasets
torch
transformers
fastapi
uvicorn
pydantic
pytest
```

### 2. Prepare the data

```bash
python src/data/preprocess.py
```

This downloads FEVER, cleans it, and writes train/validation/test splits to `data/processed/`. The same splits are used for both the ML and DL models so the comparison is fair.

### 3. Train the ML baseline

```bash
python src/models/train_ml.py
```

Trains TF-IDF + Logistic Regression and saves it to `models/fact_shift_ml.joblib`.

### 4. Train the DL model

```bash
python src/models/train_dl.py
```

Fine-tunes DistilBERT on the same splits. A GPU is strongly recommended (Google Colab or Kaggle free tier works).

### 5. Evaluate

```bash
python src/models/evaluate.py
```

Reports accuracy, macro-F1, per-class precision/recall and confusion matrices for both models.

### 6. Run the API

```bash
uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API docs.

## API

### `POST /analyze`

**Request**

```json
{ "claim": "Example factual claim" }
```

**Response**

```json
{
  "claim": "Example factual claim",
  "verdict": "NOT_ENOUGH_EVIDENCE",
  "confidence": 0.72,
  "evidence": [
    {
      "source_title": "Example source",
      "url": "https://example.com/article",
      "stance": "neutral",
      "passage": "Relevant passage from the source."
    }
  ],
  "explanation": "The available evidence is insufficient.",
  "model_version": "fact-shift-v1"
}
```

> The values above are an illustrative schema, not a real prediction. In the running system, `confidence` comes from the model and every `evidence` item comes from a retrieved source.

## Results

Results will be filled in as experiments are completed.

| Model | Accuracy | Macro-F1 | Notes |
|---|---|---|---|
| TF-IDF + Logistic Regression | _TBD_ | _TBD_ | Baseline |
| DistilBERT (fine-tuned) | _TBD_ | _TBD_ | Same splits as baseline |
| DistilBERT + retrieval + NLI | _TBD_ | _TBD_ | Full pipeline |

Error analysis, confusion matrices and examples where the two models disagree will be added to `notebooks/` and summarized here.

## Limitations

- A model trained on a labelled dataset predicts that dataset's labels. It does not independently prove a claim is true.
- FEVER is built on Wikipedia and historical claims, so performance on breaking news and other domains may be much lower.
- Retrieved sources can be outdated, biased or conflicting. Fact-Shift reports conflicts instead of hiding them.
- Confidence scores from neural networks can be miscalibrated and should not be read as probabilities of truth.
- This is a learning and portfolio project, **not** a replacement for professional fact-checkers.

## Responsible AI

- The system can return **NOT_ENOUGH_EVIDENCE** rather than forcing a true/false answer.
- Every verdict is traceable to a source URL and passage.
- No fabricated sources or placeholder confidence values.

## Testing

```bash
pytest tests/
```

## Docker

```bash
docker build -t fact-shift .
docker run -p 8000:8000 fact-shift
```

## Acknowledgements

- [FEVER](https://fever.ai) dataset and shared task
- [Hugging Face](https://huggingface.co) Transformers and Datasets
- [scikit-learn](https://scikit-learn.org)