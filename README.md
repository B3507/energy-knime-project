# energy-knime-project

Üniversite KNIME makine öğrenmesi projesi — **Enerji** (hane elektrik tüketimi).

Asıl ML modelleri **KNIME Analytics Platform** üzerinde kurulur.  
Cursor/Python: veri inceleme, temizleme, rapor ve KNIME workflow planı.

## Beş ML problemi

1. Kümeleme (`01_Kumeleme_Enerji`) — **tamamlandı (rapor + görseller)**
2. Regresyon
3. Sınıflandırma
4. Birliktelik kuralı
5. Anomali tespiti

## Klasör yapısı

```
energy-knime-project/
├── data/           # Veri (hourly CSV repoda; ham/clean yerel)
├── analysis/       # Python EDA / temizleme / doğrulama
├── knime/          # KNIME planları (+ export .knwf)
├── screenshots/    # Ekran görüntüleri
└── report/         # Ödev raporu (.md / .docx)
```

## Veri

| Dosya | Repo? | Açıklama |
| --- | --- | --- |
| `data/household_power_hourly.csv` | Evet (~5 MB) | KNIME için önerilen temiz saatlik veri |
| `data/household_power_clean.csv` | Hayır (büyük) | Dakika çözünürlüğü — yerel |
| `data/household_power_consumption.txt` | Hayır (büyük) | Ham UCI veri — yerel |

Ham veriyi yerelde tut; temizleme: `analysis/clean_household_power.py`

## Python ortamı

```powershell
python -m venv .venv
.\activate.bat
pip install pandas numpy matplotlib scikit-learn python-docx
```

## KNIME

1. `data/household_power_hourly.csv` oku (delimiter `,`)
2. Plan: `knime/01_Clustering_PLAN.md`
3. Workflow export: `knime/EXPORT_WORKFLOW.md`

## Kümeleme raporu

- Markdown: `report/RAPOR_Kumeleme.md`
- Word: `report/RAPOR_Kumeleme.docx`
- Screenshot’lar: `screenshots/`
