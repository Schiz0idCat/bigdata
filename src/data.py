#!/usr/bin/env python3
"""Descarga data/movies.csv desde Kaggle si todavía no existe."""

import shutil
from pathlib import Path

import kagglehub

DATASET = "asaniczka/tmdb-movies-dataset-2023-930k-movies"
DEST = Path("data/movies.csv")

if DEST.exists():
    print(f"Ya existe {DEST}")
else:
    path = Path(kagglehub.dataset_download(DATASET))
    csv = next(path.rglob("*.csv"))
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(csv, DEST)
    print(f"Descargado en {DEST}")
