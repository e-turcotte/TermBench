# Train a Binary Text Classifier

You have been provided a dataset of SMS messages in `/app/data/`. Your goal is
to train a binary text classifier that distinguishes spam messages from
legitimate ones.

## Dataset

The dataset is split into two files:
- `/app/data/train.csv` — training data with columns `text` and `label`
- `/app/data/val.csv` — validation data with columns `text` and `label`

Labels are `ham` for legitimate (ham) and `spam` for spam.

## Requirements

Train a classifier and save your predictions on the validation set to
`/app/predictions.csv`. The file must:
- Have a single column named `label`
- Contain exactly one prediction per row
- Be in the same order as `/app/data/val.csv`

## Constraints

- You may only use Python
- You may only use packages already installed in the environment
- Do not read from or write to any path outside `/app`
- Your solution must complete within the agent timeout
