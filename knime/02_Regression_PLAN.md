# 02_Regression — KNIME Workflow Tasarımı

**Problem:** Regresyon (supervised)  
**Hedef:** `Global_active_power` (kW) — hane aktif güç tüketimi  
**Veri:** `data/household_power_hourly.csv`  
**KNIME workflow adı:** `02_Regression`  
**Kapsam:** Node listesi, sıra, ayarlar — sonuç tahmin etmez.

---

## Amaç

Saatlik gözlemlerde **Global_active_power** değerini diğer özelliklerden tahmin etmek.

---

## Ana node zinciri (kesin sıra)

```
CSV Reader
↓
Column Filter
↓
Partitioning                 (Train %70 / Test %30)
↓
Normalizer (Min-Max)         (opsiyonel ama Linear Regression için önerilir)
↓
─────────────────────────────┬─────────────────────────────
                             │
                    Linear Regression Learner
                             │ (model)
                             ▼
                    Regression Predictor  ←── Test set (normalize edilmiş)
                             │
                             ▼
                    Numeric Scorer
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         Scatter Plot   Line Plot      Table View
         (Actual vs     (isteğe bağlı)
          Predicted)
```

**Alternatif / karşılaştırma dalı (önerilir):**

```
Partitioning (aynı split)
↓
Normalizer
↓
Tree Ensemble Learner (Regression)   veya   Random Forest Learner
↓
Regression Predictor
↓
Numeric Scorer
```

İki modelin skorlarını tabloda karşılaştır (R², MAE, RMSE).

---

## 1. Kullanılacak KNIME node’ları

| Sıra | Node | Amaç |
| --- | --- | --- |
| 1 | **CSV Reader** | Saatlik CSV |
| 2 | **Column Filter** | Hedef + özellikler |
| 3 | **Partitioning** | Train / Test ayır |
| 4 | **Normalizer** | Ölçekleme (Linear Reg için) |
| 5 | **Linear Regression Learner** | Model 1 |
| 6 | **Regression Predictor** | Test tahmini |
| 7 | **Numeric Scorer** | R², MAE, MSE, RMSE |
| 8 | **Scatter Plot** | Gerçek vs tahmin |
| 9 | **Tree Ensemble Learner** *(opsiyonel)* | Model 2 karşılaştırma |
| 10 | **Line Plot** *(opsiyonel)* | Zaman serisi görünümü |

> Node Repository: **Mining → Regression / Predictive** veya arama kutusu: `Linear Regression`, `Numeric Scorer`.

---

## 2. Node bağlantı sırası

```
[CSV Reader]
     |
     v
[Column Filter]
     |
     v
[Partitioning] ---- first output (Train) ----+
     |                                        |
     | second (Test)                          v
     |                                 [Normalizer]
     |                                        |
     |                         +--------------+--------------+
     |                         |                             |
     |                         v                             v
     |              [Linear Regression Learner]    [Tree Ensemble Learner]
     |                         |                             |
     |                         | model                       | model
     |                         v                             v
     +------ data ----> [Regression Predictor]     [Regression Predictor]
                               |                             |
                               v                             v
                        [Numeric Scorer]              [Numeric Scorer]
                               |
                               v
                        [Scatter Plot]
```

**Önemli:** Learner’a **Train**, Predictor’a **Test** (+ model) bağlanır.  
Normalizer’ı train’de fit edip test’e aynı modeli uygulamak için KNIME’da çoğu sürümde:

```
Partitioning
  ├─ Train → Normalizer (PMML/model out) → Learner
  └─ Test  → Normalizer (Apply) / veya Normalize (Apply) node
```

Pratik kısa yol (ödev için kabul edilir): tüm veriyi normalize et → sonra Partitioning  
(daha doğru: Partition → Normalizer sadece train’de öğren).

**Önerilen pratik hat (ödev):**

```
CSV Reader → Column Filter → Partitioning → Normalizer →
Linear Regression Learner → Regression Predictor → Numeric Scorer → Scatter Plot
```

(Normalizer’ı Partitioning’den sonra train+test’e ayrı uygula veya tüm tabloyu önce normalize et.)

---

## 3. Her node’un ayarları

### 3.1 CSV Reader
| Ayar | Değer |
| --- | --- |
| File | `data/household_power_hourly.csv` |
| Delimiter | `,` |
| Header | ✓ |
| Encoding | UTF-8 |

### 3.2 Column Filter

**INCLUDE (özellikler + hedef):**
- **Hedef:** `Global_active_power`
- `Global_reactive_power`
- `Voltage`
- `Sub_metering_1`
- `Sub_metering_2`
- `Sub_metering_3`
- `Hour`
- `DayOfWeek`
- `Month`
- (isteğe bağlı) `IsWeekend`

**EXCLUDE (kullanma):**
- `Global_intensity` → hedefle çok ilişkili (**sızıntı / data leakage**)
- `Consumption_Class`, `SM1_ON`, `SM2_ON`, `SM3_ON`, `High_Load`, `Peak_Hour`  
  (bunlar hedeften türetilmiş; regresyonda hile olur)
- `Datetime`, `Year`, `Day`, `Minute` (isteğe bağlı çıkar)

### 3.3 Partitioning
| Ayar | Değer |
| --- | --- |
| Relative (%) | **70 / 30** (Train / Test) |
| Sampling | Random / Stratified değil (sürekli hedef) |
| Random seed | **42** |

### 3.4 Normalizer
| Ayar | Değer |
| --- | --- |
| Method | Min-Max (0–1) |
| Columns | Tüm sayısal özellikler (+ hedefi normalize etme — **hedefi Normalizer’dan çıkar**) |

> Hedef sütunu (`Global_active_power`) **normalize etme**; Learner’da target olarak orijinal kW kalsın.  
> Sadece girdi özelliklerini normalize et.

### 3.5 Linear Regression Learner
| Ayar | Değer |
| --- | --- |
| Target column | `Global_active_power` |
| Feature columns | Column Filter’daki özellikler |
| Include constant / intercept | ✓ (varsa) |

### 3.6 Regression Predictor
- Model port ← Learner  
- Data port ← Test set  

### 3.7 Numeric Scorer
| Metrik | Anlam |
| --- | --- |
| R² (R-Squared) | Açıklanan varyans (1’e yakın iyi) |
| MAE | Ortalama mutlak hata (kW) |
| MSE / RMSE | Karesel hata |

### 3.8 Scatter Plot
| Ayar | Değer |
| --- | --- |
| X | `Global_active_power` (gerçek) |
| Y | `Prediction (Global_active_power)` veya benzeri tahmin sütunu |
| İdeal | y = x çizgisine yakın noktalar |

---

## 4. Kullanılacak sütunlar (özet)

| Rol | Sütun |
| --- | --- |
| **Hedef (Y)** | Global_active_power |
| **Özellikler (X)** | Global_reactive_power, Voltage, Sub_metering_1/2/3, Hour, DayOfWeek, Month [, IsWeekend] |
| **Yasak** | Global_intensity, Consumption_Class, SM*_ON, High_Load, Peak_Hour |

---

## 5. Normalizasyon gerekli mi?

| Model | Normalizer |
| --- | --- |
| Linear Regression | **Evet** (özellikler) |
| Tree / Random Forest | Gerekmez |

---

## 6. Değerlendirme

Test set üzerinde **Numeric Scorer** çıktısını not et:

| Model | R² | MAE | RMSE | Not |
| --- | --- | --- | --- | --- |
| Linear Regression |  |  |  |  |
| Tree Ensemble *(opsiyonel)* |  |  |  |  |

---

## 7. Görselleştirme

| Node | Ne gösterir |
| --- | --- |
| Scatter Plot | Gerçek vs tahmin |
| Table View | Katsayılar / tahmin örnekleri |
| Line Plot | İsteğe bağlı zaman sırası |

Screenshot’lar → `screenshots/02_regression_*.png`  
Rapor → `report/RAPOR_Regresyon.md` (sonra)

---

## Cursor’dan gelen node listesi (kopyala-yapıştır)

1. CSV Reader  
2. Column Filter  
3. Partitioning  
4. Normalizer  
5. Linear Regression Learner  
6. Regression Predictor  
7. Numeric Scorer  
8. Scatter Plot  
9. Tree Ensemble Learner *(opsiyonel)*  
10. Table View *(opsiyonel)*  

**Minimum sıra:**

```
CSV Reader
↓
Column Filter
↓
Partitioning
↓
Normalizer
↓
Linear Regression Learner
↓
Regression Predictor
↓
Numeric Scorer
↓
Scatter Plot
```

---

## KNIME’da senin adımların

1. New Workflow → **`02_Regression`**
2. Yukarıdaki node’ları ekle ve bağla
3. Intensity ve türetilmiş sınıfları **çıkar**
4. Execute → Numeric Scorer + Scatter screenshot al
5. Export → `knime/02_Regression.knwf`
