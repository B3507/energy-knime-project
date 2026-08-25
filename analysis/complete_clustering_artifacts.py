"""Kümeleme rapor eksiklerini tamamla — görseller + orijinal birim profilleri.
KNIME modelinin yerine geçmez; rapor/doğrulama desteğidir (aynı k=3, Min-Max, seed=42).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "household_power_hourly.csv"
SHOT = ROOT / "screenshots"
SHOT.mkdir(exist_ok=True)

FEATURES = [
    "Year",
    "Month",
    "Day",
    "Hour",
    "DayOfWeek",
    "IsWeekend",
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3",
    "SM1_ON",
    "SM2_ON",
    "SM3_ON",
    "High_Load",
    "Peak_Hour",
]

PROFILE_COLS = [
    "Global_active_power",
    "Global_reactive_power",
    "Voltage",
    "Global_intensity",
    "Sub_metering_1",
    "Sub_metering_2",
    "Sub_metering_3",
    "Hour",
    "SM3_ON",
    "High_Load",
    "Peak_Hour",
]


def main() -> None:
    df = pd.read_csv(DATA)
    X_raw = df[FEATURES].astype(float)
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X_raw)

    km = KMeans(n_clusters=3, random_state=42, n_init=10, max_iter=100)
    labels = km.fit_predict(X)
    df = df.copy()
    df["Cluster"] = labels

    # --- profiles original units ---
    prof = df.groupby("Cluster")[PROFILE_COLS].mean()
    sizes = df["Cluster"].value_counts().sort_index()
    prof_path = ROOT / "analysis" / "clustering_profiles_original.csv"
    out = prof.copy()
    out.insert(0, "count", sizes.values)
    out.to_csv(prof_path)
    print("profiles:", prof_path)
    print(out.round(4).to_string())

    # --- silhouette k=2..5 chart ---
    sil_scores = []
    rng = np.random.RandomState(42)
    idx = rng.choice(len(X), size=min(10000, len(X)), replace=False)
    for k in [2, 3, 4, 5]:
        lab = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=100).fit_predict(X)
        sil = silhouette_score(X[idx], lab[idx])
        sil_scores.append((k, sil))
        print(f"k={k} sil={sil:.4f}")

    fig, ax = plt.subplots(figsize=(7, 4))
    ks = [k for k, _ in sil_scores]
    ss = [s for _, s in sil_scores]
    bars = ax.bar([str(k) for k in ks], ss, color=["#6b7280", "#2563eb", "#6b7280", "#6b7280"])
    bars[1].set_color("#2563eb")
    ax.set_xlabel("k (küme sayısı)")
    ax.set_ylabel("Silhouette skoru")
    ax.set_title("k karşılaştırması — Silhouette (saatlik veri, Min-Max, seed=42)")
    ax.set_ylim(0, max(ss) * 1.25)
    for i, s in enumerate(ss):
        ax.text(i, s + 0.005, f"{s:.3f}", ha="center", fontsize=10)
    ax.axhline(ss[1], color="#2563eb", linestyle="--", linewidth=0.8, alpha=0.5)
    fig.tight_layout()
    p = SHOT / "01_clustering_silhouette.png"
    fig.savefig(p, dpi=140)
    plt.close()
    print("saved", p)

    # --- scatter ---
    fig, ax = plt.subplots(figsize=(7.5, 5))
    colors = {0: "#1d4ed8", 1: "#b45309", 2: "#047857"}
    for c in sorted(df["Cluster"].unique()):
        m = df["Cluster"] == c
        ax.scatter(
            df.loc[m, "Global_active_power"],
            df.loc[m, "Sub_metering_3"],
            s=8,
            alpha=0.35,
            c=colors[c],
            label=f"cluster_{c} (n={m.sum()})",
        )
    ax.set_xlabel("Global_active_power (kW)")
    ax.set_ylabel("Sub_metering_3 (Wh)")
    ax.set_title("Kümeleme Scatter — GAP vs Sub_metering_3 (k=3)")
    ax.legend(markerscale=2, frameon=False)
    fig.tight_layout()
    p = SHOT / "01_clustering_scatter.png"
    fig.savefig(p, dpi=140)
    plt.close()
    print("saved", p)

    # --- pie sizes ---
    fig, ax = plt.subplots(figsize=(6, 5))
    labels_pie = [f"cluster_{i}\n{sizes[i]:,}" for i in sizes.index]
    ax.pie(
        sizes.values,
        labels=labels_pie,
        autopct="%1.1f%%",
        colors=[colors[i] for i in sizes.index],
        startangle=90,
    )
    ax.set_title("Küme boyutları (saatlik, k=3)")
    fig.tight_layout()
    p = SHOT / "01_clustering_pie.png"
    fig.savefig(p, dpi=140)
    plt.close()
    print("saved", p)

    # --- profile bar (original units GAP) ---
    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.arange(3)
    ax.bar(x, prof["Global_active_power"].values, color=[colors[i] for i in range(3)])
    ax.set_xticks(x)
    ax.set_xticklabels([f"cluster_{i}" for i in range(3)])
    ax.set_ylabel("Ortalama Global_active_power (kW)")
    ax.set_title("Küme profilleri — ortalama aktif güç (orijinal birim)")
    for i, v in enumerate(prof["Global_active_power"].values):
        ax.text(i, v + 0.02, f"{v:.3f}", ha="center")
    fig.tight_layout()
    p = SHOT / "01_clustering_profiles.png"
    fig.savefig(p, dpi=140)
    plt.close()
    print("saved", p)

    # --- workflow diagram ---
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")
    ax.set_title("01_Kumeleme_Enerji — Node yapısı", fontsize=14, pad=12)

    boxes = [
        (3.5, 11, "CSV Reader"),
        (3.5, 10, "String Manipulation"),
        (3.5, 9, "String to Date&Time"),
        (3.5, 8, "Date&Time Part Extractor"),
        (3.5, 7, "GroupBy"),
        (3.5, 6, "Column Filter"),
        (3.5, 5, "Normalizer"),
        (3.5, 4, "k-Means"),
        (3.5, 3, "Cluster Assigner"),
        (0.8, 1.5, "Scatter / Color"),
        (3.5, 1.5, "Silhouette"),
        (6.5, 1.5, "GroupBy / Pie"),
    ]
    for x0, y0, text in boxes:
        ax.add_patch(
            plt.Rectangle(
                (x0, y0 - 0.35),
                2.8,
                0.7,
                fill=True,
                facecolor="#f3f4f6",
                edgecolor="#111827",
                linewidth=1.2,
            )
        )
        ax.text(x0 + 1.4, y0, text, ha="center", va="center", fontsize=9)

    for y in [10.5, 9.5, 8.5, 7.5, 6.5, 5.5, 4.5, 3.5]:
        ax.annotate("", xy=(4.9, y - 0.5), xytext=(4.9, y), arrowprops=dict(arrowstyle="->", color="#374151"))
    ax.annotate("", xy=(2.2, 1.85), xytext=(4.2, 2.65), arrowprops=dict(arrowstyle="->", color="#374151"))
    ax.annotate("", xy=(4.9, 1.85), xytext=(4.9, 2.65), arrowprops=dict(arrowstyle="->", color="#374151"))
    ax.annotate("", xy=(7.6, 1.85), xytext=(5.6, 2.65), arrowprops=dict(arrowstyle="->", color="#374151"))

    fig.tight_layout()
    p = SHOT / "01_clustering_workflow.png"
    fig.savefig(p, dpi=140, facecolor="white")
    plt.close()
    print("saved", p)

    print("DONE")


if __name__ == "__main__":
    main()
