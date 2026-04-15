import os
import pytest
import pandas as pd
from sklearn.metrics import f1_score

F1_THRESHOLD = 0.98
PREDICTIONS_PATH = "/app/predictions.csv"
HIDDEN_LABELS_PATH = "/tests/hidden_labels.csv"
VAL_DATA_PATH = "/app/data/val.csv"


def test_predictions_file_exists():
    assert os.path.exists(PREDICTIONS_PATH), \
        "predictions.csv not found at /app/predictions.csv"


def test_predictions_has_label_column():
    df = pd.read_csv(PREDICTIONS_PATH)
    assert "label" in df.columns, \
        f"predictions.csv must have a 'label' column, got: {list(df.columns)}"


def test_predictions_correct_length():
    predictions = pd.read_csv(PREDICTIONS_PATH)
    val = pd.read_csv(VAL_DATA_PATH)
    assert len(predictions) == len(val), \
        f"Expected {len(val)} predictions, got {len(predictions)}"


def test_predictions_are_binary():
    df = pd.read_csv(PREDICTIONS_PATH)
    unique_values = set(df["label"].unique())
    assert unique_values.issubset({'ham', 'spam'}), \
        f"Labels must be \'ham\' or \'spam\', got: {unique_values}"


def test_predictions_no_nulls():
    df = pd.read_csv(PREDICTIONS_PATH)
    assert df["label"].isnull().sum() == 0, \
        "predictions.csv contains null values"


def test_f1_score_meets_threshold():
    predictions = pd.read_csv(PREDICTIONS_PATH)
    hidden = pd.read_csv(HIDDEN_LABELS_PATH)
    score = f1_score(hidden["label"], predictions["label"], pos_label='ham')
    assert score >= F1_THRESHOLD, \
        f"F1 score {score:.4f} is below required threshold of {F1_THRESHOLD}""""
Use this file to define pytest tests that verify the outputs of the task.

This file will be copied to /tests/test_outputs.py and run by the /tests/test.sh file
from the working directory.
"""


def test_outputs():
    """Test that the outputs are correct."""
    pass
