"""EDA for household_power_consumption.txt — no ML training."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "household_power_consumption.txt"
OUT = Path(__file__).resolve().parent / "eda_report.json"

NUMERIC_COLS = [
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3",
]


def main() -> None:
    size_bytes = DATA.stat().st_size

    # Line count including header
    with DATA.open("r", encoding="utf-8", errors="replace") as f:
        n_lines = sum(1 for _ in f)
    n_rows = n_lines - 1  # data rows

    # Read with KNIME-relevant parsing rules
    df = pd.read_csv(
        DATA,
        sep=";",
        na_values=["?", ""],
        low_memory=False,
    )

    cols = list(df.columns)
    n_cols = len(cols)

    # Raw string dtype before conversion (as in file)
    raw_dtypes = {c: str(df[c].dtype) for c in cols}

    # Convert numerics (file stores them as object if mixed / ?)
    for c in NUMERIC_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    missing = df.isna().sum()
    missing_pct = (missing / len(df) * 100).round(4)

    # Date / Time checks
    date_ok = pd.to_datetime(df["Date"], format="%d/%m/%Y", errors="coerce")
    time_ok = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce")
    date_parse_fail = int(date_ok.isna().sum())
    time_parse_fail = int(time_ok.isna().sum())

    datetime_combined = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce",
    )
    dt_min = str(datetime_combined.min()) if datetime_combined.notna().any() else None
    dt_max = str(datetime_combined.max()) if datetime_combined.notna().any() else None

    numeric_stats = {}
    for c in NUMERIC_COLS:
        s = df[c]
        numeric_stats[c] = {
            "dtype_after_cast": str(s.dtype),
            "missing": int(s.isna().sum()),
            "missing_pct": round(float(s.isna().mean() * 100), 4),
            "min": None if s.dropna().empty else float(s.min()),
            "max": None if s.dropna().empty else float(s.max()),
            "mean": None if s.dropna().empty else float(s.mean()),
            "median": None if s.dropna().empty else float(s.median()),
            "std": None if s.dropna().empty else float(s.std()),
        }

    # Sample of '?' presence in raw file (first chunk check already handled via na_values)
    # Count rows with any missing among numeric
    any_missing_numeric = int(df[NUMERIC_COLS].isna().any(axis=1).sum())

    report = {
        "file": str(DATA),
        "size_bytes": size_bytes,
        "size_mb": round(size_bytes / (1024 * 1024), 2),
        "n_lines_including_header": n_lines,
        "n_data_rows": n_rows,
        "n_columns": n_cols,
        "column_names": cols,
        "raw_dtypes_as_read": raw_dtypes,
        "separator": ";",
        "missing_token": "?",
        "date_format": "dd/MM/yyyy",
        "time_format": "HH:mm:ss",
        "datetime_range": {"min": dt_min, "max": dt_max},
        "date_parse_failures": date_parse_fail,
        "time_parse_failures": time_parse_fail,
        "missing_count": {c: int(missing[c]) for c in cols},
        "missing_pct": {c: float(missing_pct[c]) for c in cols},
        "rows_with_any_numeric_missing": any_missing_numeric,
        "numeric_columns": NUMERIC_COLS,
        "datetime_columns": ["Date", "Time"],
        "numeric_stats": numeric_stats,
        "units_hint": {
            "Global_active_power": "kW",
            "Global_reactive_power": "kW",
            "Voltage": "V",
            "Global_intensity": "A",
            "Sub_metering_1": "Wh (kitchen)",
            "Sub_metering_2": "Wh (laundry)",
            "Sub_metering_3": "Wh (water heater / AC)",
        },
    }

    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
