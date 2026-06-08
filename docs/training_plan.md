# Training And Evaluation Plan

## Goal

Train a multi-modal fake news and deepfake detection system that fuses text, image, source, and claim evidence.

## Datasets

- FakeNewsNet: article text, publisher metadata, and social context
- LIAR: short political claim classification
- Kaggle Fake and Real News: large-scale article classification
- DFDC, FaceForensics++, Celeb-DF: manipulated video/image detection
- PolitiFact or Snopes-derived evidence snippets for claim verification

## Model Architecture

1. Text encoder:
   - Start with DistilBERT for speed
   - Upgrade to DeBERTa-v3 or RoBERTa for stronger performance
   - Output calibrated fake probability and embedding

2. Image encoder:
   - Start with EfficientNet-B0 or XceptionNet
   - Upgrade to ViT or ConvNeXt for richer image features
   - Train on manipulated vs authentic media

3. Claim verifier:
   - Encode claim and evidence with sentence-transformers
   - Use retrieval similarity plus entailment classification

4. Source model:
   - Use domain reputation, age, historical fact-checks, and publisher metadata

5. Fusion model:
   - Concatenate modality embeddings and calibrated probabilities
   - Train logistic regression, gradient boosting, or a small MLP
   - Compare early fusion and late fusion

## Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1 score
- ROC-AUC
- Calibration error
- Confusion matrix by topic and source group

## Explainability

- Use SHAP for fusion-level feature contribution
- Use LIME or integrated gradients for text tokens
- Use Grad-CAM or attention rollout for image regions
- Surface top evidence snippets for claim verification

## Amazon ML School Talking Points

- Clear problem framing with multiple data modalities
- Strong baseline before complex models
- Error analysis and calibration, not just accuracy
- Ethical deployment and human-in-the-loop review
- Modular design that supports ablation studies
- Metrics aligned to false-positive and false-negative costs
