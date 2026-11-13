# Descargar el dataset
`src/data.py` baja el dataset de Kaggle y deja el CSV en `data/movies.csv`
(crea `data/` si no existe; no descarga nada si el archivo ya está):

```bash
uv run python src/data.py
```

# Alcance
En base a [requerimientos](./docs/requerimientos.pdf),
se desarrollará una IA capaz de predecir el **revenue real** (dólares constantes de 2025)
a partir de columnas del CSV disponibles antes del estreno. El año de estreno se usa
solo para separar entrenamiento y evaluación, no como variable predictora.

# Inflación (CPI)
`data/cpi_us.csv` contiene el CPI-U anual (FRED `CPIAUCNS`, promedio anual) y se usa
para deflactar `revenue` y `budget` a dólares de 2025:

```bash
uv run python src/build_cpi.py   # regenera el CPI (opcional; el CSV ya está versionado)
```

El año base es 2025. FRED no publicó 2025-10, así que ese mes se interpola como
`(2025-09 + 2025-11) / 2` en `src/build_cpi.py`; 2026 queda fuera por estar incompleto.
