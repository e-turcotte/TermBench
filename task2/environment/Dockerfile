FROM python:3.11-slim

RUN pip install --no-cache-dir \
    scikit-learn \
    pandas \
    numpy \
    pytest

WORKDIR /app
COPY data/ /app/data/
