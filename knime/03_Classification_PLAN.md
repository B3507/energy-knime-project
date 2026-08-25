# 03_Classification — KNIME Workflow Tasarımı

**Problem:** Sınıflandırma (supervised)  
**Hedef:** `Consumption_Class` (Low / Medium / High) — GAP’ten türetilmiş  
**Veri:** `data/household_power_hourly.csv`  
**KNIME workflow adı:** `03_Classification` / `03_Siniflandirma_Enerji`  
**Kapsam:** Node listesi ve ayarlar — skor tahmin etmez.

---

## Amaç

Saatlik gözlemleri **düşük / orta / yüksek** tüketim sınıflarına ayırmak.

> `Consumption_Class` dosyada zaten var (temizleme sırasında üretildi).  
> **Dikkat:** Hedef GAP eşiklerinden geldiği için özelliklerde **Global_active_power**, **Global_intensity**, **High_Load**, **Peak_Hour** kullanma (sızıntı).

---

## Olması gereken node yapısı

```
CSV Reader
    ↓
Column Filter
    ↓
Partitioning                    (%70 Train / %30 Test, seed 42)
   ╱                          ╲
Train                         Test
   ↓                            ╲
Decision Tree Learner            ╲
   │ (model)                      ╲
   └──────────► Decision Tree Predictor
                         ↓
                   Scorer (Java)
                         ↓
              ┌──────────┴──────────┐
              ▼                     ▼
         Confusion Matrix      Pie Chart / ROC
         (Scorer View)         (isteğe bağlı)
```

**Alternatif model (karşılaştırma):** `Random Forest Learner` → `Random Forest Predictor` → Scorer

---

## Node listesi

1. **CSV Reader**  
2. **Column Filter**  
3. **Partitioning** (Table Partitioner)  
4. **Decision Tree Learner**  
5. **Decision Tree Predictor**  
6. **Scorer**  
7. *(opsiyonel)* Random Forest Learner + Predictor  
8. *(opsiyonel)* ROC Curve  

---

## Column Filter

**INCLUDE**
- **Hedef:** `Consumption_Class`
- `Global_reactive_power`
- `Voltage`
- `Sub_metering_1`, `Sub_metering_2`, `Sub_metering_3`
- `Hour`, `DayOfWeek`, `Month`
- (isteğe bağlı) `IsWeekend`

**EXCLUDE (sızıntı)**
- `Global_active_power` ← sınıftan doğrudan türetilmiş
- `Global_intensity`
- `High_Load`, `Peak_Hour`
- `SM1_ON`, `SM2_ON`, `SM3_ON` (istersen özellik olarak bırakılabilir; SM*_ON sınıf sızıntısı değil ama basit tut)

---

## Learner ayarları

| Ayar | Değer |
| --- | --- |
| Class column | `Consumption_Class` |
| Features | Include listesindeki sayısal sütunlar |
| Partitioning | 70/30, seed 42 |

---

## Değerlendirme (Scorer)

Not edilecekler:
- Accuracy  
- Confusion Matrix (Low/Medium/High)  
- Precision / Recall / F1 (sınıf bazlı, View’da)

---

## Minimum sıra (kopyala)

```
CSV Reader
↓
Column Filter
↓
Partitioning
↓
Decision Tree Learner          ← Train
↓
Decision Tree Predictor        ← model + Test
↓
Scorer
```

---

## KNIME’da senin adımların

1. New Workflow → `03_Siniflandirma_Enerji`
2. Yukarıdaki node’ları kur
3. GAP / Intensity / High_Load’u **çıkar**
4. Execute → Scorer View → screenshot
5. Export → `knime/03_Classification.knwf`
