"""
KNIME için veri temizleme — ML eğitimi yok.
Girdi: data/household_power_consumption.txt
Çıktı:
  - data/household_power_clean.csv      (dakika, temiz)
  - data/household_power_hourly.csv     (saatlik özet, KNIME için önerilen)
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "household_power_consumption.txt"
OUT_CLEAN = ROOT / "data" / "household_power_clean.csv"
OUT_HOURLY = ROOT / "data" / "household_power_hourly.csv"

NUMERIC = [
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3",
]


def main() -> None:
    print("Reading raw file...")
    df = pd.read_csv(
        SRC,
        sep=";",
        na_values=["?", ""],
        low_memory=False,
    )
    n0 = len(df)
    print(f"  rows_raw={n0:,}")

    for c in NUMERIC:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Drop rows where any measurement is missing (same 25,979 gap rows)
    before = len(df)
    df = df.dropna(subset=NUMERIC).copy()
    dropped = before - len(df)
    print(f"  dropped_missing={dropped:,}  rows_clean={len(df):,}")

    # Date + Time → Datetime
    df["Datetime"] = pd.to_datetime(
        df["Date"].astype(str) + " " + df["Time"].astype(str),
        format="%d/%m/%Y %H:%M:%S",
        errors="coerce",
    )
    bad_dt = int(df["Datetime"].isna().sum())
    if bad_dt:
        df = df.dropna(subset=["Datetime"]).copy()
        print(f"  dropped_bad_datetime={bad_dt:,}")

    # Extract time fields
    df["Year"] = df["Datetime"].dt.year
    df["Month"] = df["Datetime"].dt.month
    df["Day"] = df["Datetime"].dt.day
    df["Hour"] = df["Datetime"].dt.hour
    df["Minute"] = df["Datetime"].dt.minute
    df["DayOfWeek"] = df["Datetime"].dt.dayofweek  # 0=Mon … 6=Sun
    df["IsWeekend"] = (df["DayOfWeek"] >= 5).astype(int)

    # Classification target (for KNIME Rule Engine parity)
    df["Consumption_Class"] = pd.cut(
        df["Global_active_power"],
        bins=[-float("inf"), 0.5, 2.0, float("inf")],
        labels=["Low", "Medium", "High"],
    ).astype(str)

    # Association / binary flags
    df["SM1_ON"] = (df["Sub_metering_1"] > 0).astype(int)
    df["SM2_ON"] = (df["Sub_metering_2"] > 0).astype(int)
    df["SM3_ON"] = (df["Sub_metering_3"] > 0).astype(int)
    df["High_Load"] = (df["Global_active_power"] > 2.0).astype(int)
    df["Peak_Hour"] = ((df["Hour"] >= 18) & (df["Hour"] <= 22)).astype(int)

    # Column order for KNIME
    cols = [
        "Datetime",
        "Date",
        "Time",
        "Year",
        "Month",
        "Day",
        "Hour",
        "Minute",
        "DayOfWeek",
        "IsWeekend",
        *NUMERIC,
        "Consumption_Class",
        "SM1_ON",
        "SM2_ON",
        "SM3_ON",
        "High_Load",
        "Peak_Hour",
    ]
    df = df[cols].sort_values("Datetime").reset_index(drop=True)

    print(f"Writing {OUT_CLEAN.name} ...")
    df.to_csv(OUT_CLEAN, index=False, sep=",")
    print(f"  size_mb={OUT_CLEAN.stat().st_size / (1024*1024):.1f}")

    # Hourly aggregation (KNIME-friendly size)
    print("Building hourly aggregate...")
    g = df.set_index("Datetime").resample("h")
    hourly = g.agg(
        {
            "Global_active_power": "mean",
            "Global_reactive_power": "mean",
            "Voltage": "mean",
            "Global_intensity": "mean",
            "Sub_metering_1": "sum",
            "Sub_metering_2": "sum",
            "Sub_metering_3": "sum",
            "IsWeekend": "max",
            "SM1_ON": "max",
            "SM2_ON": "max",
            "SM3_ON": "max",
            "High_Load": "max",
            "Peak_Hour": "max",
        }
    ).dropna(subset=["Global_active_power"]).reset_index()

    hourly["Year"] = hourly["Datetime"].dt.year
    hourly["Month"] = hourly["Datetime"].dt.month
    hourly["Day"] = hourly["Datetime"].dt.day
    hourly["Hour"] = hourly["Datetime"].dt.hour
    hourly["DayOfWeek"] = hourly["Datetime"].dt.dayofweek
    hourly["Consumption_Class"] = pd.cut(
        hourly["Global_active_power"],
        bins=[-float("inf"), 0.5, 2.0, float("inf")],
        labels=["Low", "Medium", "High"],
    ).astype(str)

    hourly_cols = [
        "Datetime",
        "Year",
        "Month",
        "Day",
        "Hour",
        "DayOfWeek",
        "IsWeekend",
        *NUMERIC,
        "Consumption_Class",
        "SM1_ON",
        "SM2_ON",
        "SM3_ON",
        "High_Load",
        "Peak_Hour",
    ]
    hourly = hourly[hourly_cols]

    print(f"Writing {OUT_HOURLY.name} ...")
    hourly.to_csv(OUT_HOURLY, index=False, sep=",")
    print(f"  rows_hourly={len(hourly):,}")
    print(f"  size_mb={OUT_HOURLY.stat().st_size / (1024*1024):.1f}")

    print("DONE")
    print(
        {
            "rows_raw": n0,
            "rows_clean": len(df),
            "dropped_missing": dropped,
            "rows_hourly": len(hourly),
            "class_counts": df["Consumption_Class"].value_counts().to_dict(),
        }
    )


if __name__ == "__main__":
    main()
