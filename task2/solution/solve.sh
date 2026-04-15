#!/bin/bash
set -e

python3 - << 'EOF'
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Load data
train = pd.read_csv("/app/data/train.csv")
val = pd.read_csv("/app/data/val.csv")

# Build and train pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=50000,
        sublinear_tf=True
    )),
    ("clf", LogisticRegression(
        C=10,
        max_iter=1000,
        solver="lbfgs"
    ))
])

pipeline.fit(train["text"], train["label"])

# Generate predictions on validation set
predictions = pipeline.predict(val["text"])

# Save predictions
pd.DataFrame({"label": predictions}).to_csv("/app/predictions.csv", index=False)

print("Done. Predictions saved to /app/predictions.csv")
EOF
