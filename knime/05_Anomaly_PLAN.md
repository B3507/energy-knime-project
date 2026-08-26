# 05_Anomaly — KNIME Workflow Tasarımı

**Problem:** Anomali tespiti (outlier / anomaly detection)  
**Veri:** `data/household_power_hourly.csv` (önerilen)  
**KNIME workflow adı:** `05_Anomali_Enerji`  
**Kapsam:** Node listesi ve ayarlar — sonuç tahmin etmez.

---

## Amaç

Normal tüketimden sapan gözlemleri bulmak  
(ani güç sıçraması, anormal gerilim, aşırı yük vb.).

---

## Olması gereken node yapısı

```
CSV Reader
    ↓
Column Filter
    ↓
Normalizer                 (Min-Max — mesafe tabanlı yöntemler için)
    ↓
Numeric Outliers           (IQR / z-score — basit ve ödev için net)
    ↓
Row Filter                 (outlier flag = true olanlar)  [isteğe bağlı]
    ↓
Scatter Plot / Table View
```

**Alternatif / ek dal (varsa node):**

```
Column Filter → Normalizer → Isolation Forest / DBSCAN / Local Outlier Factor
                         → Table View / Scatter Plot
```

KNIME Community / Extensions’ta `Isolation Forest`, `LOF`, `DBSCAN` aranabilir.  
Yoksa **Numeric Outliers** yeterlidir.

---

## Pratik minimum hat (önerilen)

```
CSV Reader
↓
Column Filter
↓
Normalizer
↓
Numeric Outliers
↓
Color Manager          (outlier flag’e göre renk)
↓
Scatter Plot
↓
GroupBy / Table View   (kaç anomali?)
```

---

## 1. CSV Reader
| Ayar | Değer |
| --- | --- |
| File | `household_power_hourly.csv` |
| Delimiter | `,` |
| Header | ✓ |

---

## 2. Column Filter — kullanılacak sütunlar

**INCLUDE (anomali için):**
- `Global_active_power`
- `Voltage`
- `Global_intensity` *(burada sızıntı yok — hedef yok; anomali için kullanılabilir)*
- `Sub_metering_1`, `Sub_metering_2`, `Sub_metering_3`
- (isteğe bağlı) `Hour` — görselleştirme için Join ile geri ekle

**EXCLUDE:**
- `Consumption_Class`, `SM*_ON`, `High_Load`, `Peak_Hour` (etiket; anomali girişine şart değil)
- Ham `Datetime` (istersen sakla, modele koyma)

---

## 3. Normalizer
| Ayar | Değer |
| --- | --- |
| Method | Min-Max (0–1) |
| Columns | Seçilen sayısal ölçümler |

---

## 4. Numeric Outliers
| Ayar | Öneri |
| --- | --- |
| Method | **IQR** (çeyrekler açıklığı) veya z-score |
| Columns | Global_active_power, Voltage, (opsiyonel Intensity / SM) |
| Output | Outlier flag sütunu (true/false) veya işaretli satırlar |

IQR kuralı (klasik):  
`değer < Q1 - 1.5×IQR` veya `değer > Q3 + 1.5×IQR` → outlier

---

## 5. Değerlendirme / görsel

| Ne | Nasıl |
| --- | --- |
| Anomali sayısı | GroupBy / Value Counter (flag) |
| Oran | anomaly_count / total |
| Görsel | Scatter: X=Hour veya GAP, Y=Voltage; Color=outlier |
| Tablo | Outlier satırlarının GAP/Voltage ortalaması |

Rapor tablosu:

| Metrik | Değer |
| --- | --- |
| Toplam satır |  |
| Anomali sayısı |  |
| Anomali oranı (%) |  |
| Yöntem | Numeric Outliers (IQR) |

---

## Cursor’dan node listesi

1. CSV Reader  
2. Column Filter  
3. Normalizer  
4. Numeric Outliers  
5. Color Manager  
6. Scatter Plot  
7. Table View / GroupBy  

**Minimum sıra:**

```
CSV Reader
↓
Column Filter
↓
Normalizer
↓
Numeric Outliers
↓
Scatter Plot
```

---

## KNIME’da senin adımların

1. New Workflow → **`05_Anomali_Enerji`**
2. Yukarıdaki node’ları kur  
3. Execute → outlier sayısını ve Scatter’ı kaydet  
4. Screenshot → `screenshots/05_anomaly_*.png`  
5. Export → `knime/05_Anomali_Enerji.knwf`
