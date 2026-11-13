#!/usr/bin/env python3
"""Genera data/cpi_us.csv con el CPI-U anual (base 2025).

Fuente: FRED, serie CPIAUCNS (CPI-U, all items, not seasonally adjusted),
promedio anual de los valores mensuales.

Nota sobre 2025-10: FRED no publicó ese mes (gap en la serie). Para poder usar
2025 como año base se interpola como el promedio de 2025-09 y 2025-11. Es una
interpolación puntual y documentada; no se inventan años completos.

Uso (requiere red):
    uv run python src/build_cpi.py
"""

from __future__ import annotations

import csv
import io
import urllib.request
from collections import defaultdict
from pathlib import Path

URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS"
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data" / "cpi_us.csv"


def descargar_mensual() -> dict[tuple[int, int], float]:
    with urllib.request.urlopen(URL, timeout=30) as response:
        texto = response.read().decode("utf-8")
    valores: dict[tuple[int, int], float] = {}
    for row in csv.DictReader(io.StringIO(texto)):
        fecha = row["observation_date"]
        valor = row["CPIAUCNS"]
        if valor in ("", "."):
            continue
        valores[(int(fecha[:4]), int(fecha[5:7]))] = float(valor)
    return valores


def promedio_anual(valores: dict[tuple[int, int], float], year: int) -> float | None:
    """Promedio de los 12 meses; interpola meses interiores faltantes.

    FRED no tiene 2025-10. Si falta un mes interior, se interpola con el
    promedio de sus vecinos (por eso 2025-10 = (2025-09 + 2025-11) / 2).
    Si faltan meses al final del año (p. ej. 2026), el año se descarta.
    """
    meses = {m: valores.get((year, m)) for m in range(1, 13)}

    for month, value in meses.items():
        if value is not None:
            continue
        anterior = next((meses[m] for m in range(month - 1, 0, -1) if meses[m] is not None), None)
        siguiente = next((meses[m] for m in range(month + 1, 13) if meses[m] is not None), None)
        if anterior is None or siguiente is None:
            return None
        meses[month] = (anterior + siguiente) / 2

    return sum(meses.values()) / 12


def main() -> None:
    mensual = descargar_mensual()
    years = sorted({year for year, _ in mensual})
    filas = []
    for year in range(min(years), max(years) + 1):
        promedio = promedio_anual(mensual, year)
        if promedio is not None:
            filas.append((year, f"{promedio:.3f}"))

    DEST.parent.mkdir(parents=True, exist_ok=True)
    with DEST.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["year", "cpi"])
        writer.writerows(filas)

    print(f"Escrito {DEST} con {len(filas)} años ({filas[0][0]}-{filas[-1][0]})")
    print(f"CPI base 2025: {dict(filas)[2025]}")


if __name__ == "__main__":
    main()
