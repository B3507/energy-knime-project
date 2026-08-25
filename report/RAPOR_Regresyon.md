# Regresyon Raporu
## Enerji Tüketimi — KNIME Analytics Platform

**Workflow:** `02_Regresyon_Enerji`  
**Hedef:** `Global_active_power` (kW)  
**Veri:** `data/household_power_hourly.csv`  
**Model:** Linear Regression  
**Tarih:** 25.08.2026  

---

## 1. Amaç

Saatlik hane elektrik verisinde aktif güç tüketimini (`Global_active_power`) diğer özelliklerden tahmin etmek.

---

## 2. Veri ve özellikler

| Rol | Sütunlar |
| --- | --- |
| Hedef (Y) | Global_active_power |
| Özellikler (X) | Global_reactive_power, Voltage, Sub_metering_1/2/3, Hour, DayOfWeek, Month |
| Kullanılmayan | Global_intensity (sızıntı), Consumption_Class, SM*_ON, High_Load, Peak_Hour |

**Train / Test:** Table Partitioner (~%70 / %30)  
**Normalizasyon:** Final koşumda yok (ölçek hatası riski; Linear Regression için şart değil).

---

## 3. KNIME node yapısı

```
CSV Reader
    ↓
Column Filter
    ↓
Table Partitioner
   ╱              ╲
Train             Test
   ↓                ╲
Linear Regression    ╲
Learner ────model────► Regression Predictor
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
        Numeric Scorer                 Scatter Plot
```

**Numeric Scorer (doğru ayar):**
- Reference: `Global_active_power`
- Predicted: `Prediction (Global_active_power)`

---

## 4. Sonuçlar (test seti — KNIME)

| Metrik | Değer | Yorum |
| --- | ---: | --- |
| **R²** | **0,757** | Varyansın ~%76’sı açıklanıyor |
| **Adjusted R²** | **0,757** | |
| **MAE** | **0,353** kW | Ortalama mutlak hata |
| **MSE** | **0,272** | |
| **RMSE** | **0,522** kW | |
| Mean signed difference | 0 | Sistematik sapma yok |
| MAPE | 0,563 | Düşük GAP’te şişebilir |

### Süreç notları
- İlk R²=1 → Intensity / hedef sızıntısı (düzeltildi).  
- R²&lt;0 → yanlış Prediction sütunu (`Peak_Hour`) (düzeltildi).  
- Final skor geçerli test değerlendirmesidir.

### Doğrulama (aynı özellikler, seed=42)
Saatlik CSV üzerinde aynı split ile R²≈0,75 — KNIME sonucu ile uyumlu.

---

## 5. Görseller

| Dosya | İçerik | Durum |
| --- | --- | --- |
| `screenshots/02_regression_workflow.png` | Node diyagramı | **Tamam** |
| `screenshots/02_regression_scorer.png` | Numeric Scorer | **Tamam** |
| `screenshots/02_regression_scatter.png` | Gerçek vs tahmin | **Tamam** |

Word: `report/RAPOR_Regresyon.docx`  
Workflow export: `knime/02_Regression_EXPORT.md` → `02_Regresyon_Enerji.knwf`

---

## 6. Sonuç

- Linear Regression ile `Global_active_power` tahmini KNIME’da tamamlandı.  
- Test: **R² ≈ 0,76**, **MAE ≈ 0,35 kW**, **RMSE ≈ 0,52 kW**.  
- Rapor, skor ekranı ve scatter görselleri hazır.  
- Kullanıcı adımı: KNIME’dan `.knwf` export (`02_Regression_EXPORT.md`).

---

*Yalnızca regresyon problemi.*
