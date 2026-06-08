# Multi-Modal Fake News & Deepfake Detection System

An end-to-end research-style machine learning project for detecting misinformation from text, source metadata, claims, and news images.

The project is designed for an Amazon ML School level portfolio: it demonstrates NLP, computer vision, feature fusion, ensemble scoring, explainable machine learning outputs, and evaluation planning without requiring a GPU just to run the demo.

## What It Checks

- Text credibility from headline and article body
- Image manipulation signals from uploaded news images
- Source reliability from publisher/domain patterns
- Claim verification using a lightweight evidence-matching module
- Feature fusion into a final Fake / Real probability
- Human-readable explanations for every prediction

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If you only want to run a command-line demo:

```powershell
python -m src.cli --sample samples/sample_article.json
```

## Project Structure

```text
app.py                         Streamlit interface
requirements.txt               Runtime dependencies
samples/                       Example article inputs
src/
  cli.py                       CLI inference entry point
  config.py                    Model weights and thresholds
  multimodal_detector.py       Main fusion pipeline
  models/
    text_model.py              NLP credibility model
    image_model.py             Image manipulation signal model
    source_model.py            Source reliability model
    claim_model.py             Claim verification model
  explainability.py            Explanation generation
  schemas.py                   Shared dataclasses
  utils.py                     Helpers
tests/
  test_pipeline.py             Smoke tests for the detector
docs/
  model_card.md                Model behavior, limitations, ethics
  training_plan.md             Dataset and training roadmap
```

## ML Concepts Covered

- NLP: tokenization, linguistic signals, transformer-ready model interface
- Computer Vision: image artifact analysis, CNN/ViT-ready interface
- Feature Fusion: weighted late fusion across modalities
- Ensemble Learning: independent modality scores combined into final probability
- Model Explainability: top contributing signals and natural-language rationale
- Evaluation: accuracy, precision, recall, F1, ROC-AUC

## Recommended Real Training Datasets

- FakeNewsNet for news content and social context
- LIAR for short political claims
- Kaggle Fake and Real News Dataset for article classification
- FaceForensics++, Celeb-DF, DFDC, and DeeperForensics for deepfake detection

## Important Note

This repository ships with a transparent baseline detector so the system is runnable immediately. For production or research claims, replace the baseline modules with trained BERT/DistilBERT and CNN/ViT models using the roadmap in `docs/training_plan.md`.
