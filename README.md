# Descargar el dataset
`src/data.py` baja el dataset de Kaggle y deja el CSV en `data/movies.csv`
(crea `data/` si no existe; no descarga nada si el archivo ya está):

```bash
uv run python src/download_data.py
```

# Alcance
En base a [requerimientos](./docs/requerimientos.pdf),
se desarrollará una IA capaz de predecir el revenue a partir de columnas en el csv con no tantos nulos,
dichas columnas se decidirán posteriormente.
