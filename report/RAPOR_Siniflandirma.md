# Sınıflandırma Raporu
## Enerji Tüketimi — KNIME Analytics Platform

**Workflow:** `03_Siniflandirma_Enerji`  
**Hedef:** `Consumption_Class` (Low / Medium / High)  
**Model:** Decision Tree  
**Tarih:** 25.08.2026  

---

## 1. Amaç

Tüketim gözlemlerini **düşük / orta / yüksek** sınıflarına ayırmak.

---

## 2. Özellikler

| Rol | Sütunlar |
| --- | --- |
| Hedef | Consumption_Class |
| Özellikler | Global_reactive_power, Voltage, Sub_metering_1/2/3, Hour, DayOfWeek, Month |
| Sızıntı (çıkarıldı) | Global_active_power, Global_intensity, High_Load, Peak_Hour |

Sınıf GAP eşiklerinden türetilmiştir; GAP özellikte olursa Accuracy yapay %100 olur. Final koşum sızıntısızdır.

---

## 3. Node yapısı

```
CSV Reader → Column Filter → Partitioning
     Train → Decision Tree Learner
     Test + model → Decision Tree Predictor → Scorer
```

**Scorer:** Predicted = `Prediction (Consumption_Class)` · Actual = `Consumption_Class`

---

## 4. Sonuçlar (KNIME Scorer)

| Metrik | Değer |
| --- | ---: |
| **Accuracy** | **%83,137** |
| Correct classified | 511.112 |
| Wrong classified | 103.672 |
| Error | %16,863 |
| Cohen’s kappa | **0,723** |

### Confusion Matrix

| Prediction \ Actual | High | Medium | Low |
| --- | ---: | ---: | ---: |
| **High** | **67.477** | 22.035 | 2.396 |
| **Medium** | 18.778 | **183.417** | 33.042 |
| **Low** | 1.805 | 25.614 | **260.218** |

### Yorum
Accuracy ≈ %83, kappa ≈ 0,72 — iyi ayırım. En çok karışıklık Medium sınırlarında. Sızıntı giderildikten sonra (önce %100) geçerli test sonucudur.

---

## 5. Görseller

| Dosya | Durum |
| --- | --- |
| `screenshots/03_classification_scorer.png` | **Tamam** |
| `screenshots/03_classification_workflow.png` | **Tamam** |
| `screenshots/03_classification_confusion.png` | **Tamam** |

Word: `report/RAPOR_Siniflandirma.docx`  
Export: `knime/03_Classification_EXPORT.md` → `03_Siniflandirma_Enerji.knwf`

---

## 6. Sonuç

Decision Tree ile `Consumption_Class` sınıflandırması tamamlandı.  
Test: **Accuracy ≈ %83**, **kappa ≈ 0,72**.  
Kullanıcı adımı: KNIME `.knwf` export.

---

*Yalnızca sınıflandırma.*
