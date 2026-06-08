# Model Card

## Intended Use

This system is an educational and portfolio-grade misinformation detection prototype. It helps reviewers triage suspicious news content by combining text, image, source, and claim-level signals.

## Inputs

- Headline
- Article body
- Source or publisher domain
- Primary factual claim
- Optional trusted evidence snippets
- Optional article image

## Outputs

- Fake / Real label
- Fake probability
- Confidence score
- Risk band
- Per-modality scores
- Explanation and reviewer actions

## Baseline Model

The default implementation uses transparent heuristic models so the project can run locally without trained weights. This is intentional for demo reliability. The interfaces are structured so trained models can replace each component:

- DistilBERT or DeBERTa for text credibility
- ViT, EfficientNet, or XceptionNet for image/deepfake detection
- Graph or metadata model for source reliability
- Retrieval-augmented claim verification with sentence transformers

## Limitations

- The baseline is not a production misinformation classifier.
- It can over-score satire, opinion, or unusual writing styles.
- It cannot verify facts beyond the evidence snippets provided.
- Image analysis detects broad manipulation signals, not identity-level deepfakes.
- Real deployment requires careful bias, safety, and adversarial testing.

## Ethical Use

The system should support human review, not replace it. Predictions should not be used to censor, punish, or rank publishers without transparent appeal and audit processes.
