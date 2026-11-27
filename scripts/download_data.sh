#!/usr/bin/env bash
# Downloads the organizers' Drive folder into data/raw/ and converts CSVs to parquet.
set -e
cd "$(git rev-parse --show-toplevel)"
mkdir -p data/raw data/processed
pip install -q gdown pandas pyarrow
gdown --folder "https://drive.google.com/drive/folders/1i2Ith9mfzTHyb1DX2WHSuXxeB2PCWjNM" -O data/raw
python src/prepare_data.py
