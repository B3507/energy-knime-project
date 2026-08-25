# 04_Association — KNIME Workflow Tasarımı

**Problem:** Birliktelik kuralı (Association Rules)  
**Veri:** `data/household_power_hourly.csv` (önerilen)  
**KNIME workflow adı:** `04_Birliktelik_Enerji`  
**Kapsam:** Node listesi ve ayarlar — kural skoru tahmin etmez.

---

## Amaç

Aynı saatte birlikte görülen enerji durumlarını bulmak  
(ör. `SM3_ON` + `Peak_Hour` → `High_Load`).

Ham veri sürekli olduğu için önce **ikili / kategorik item**’lara çevrilir.

---

## Olması gereken node yapısı

```
CSV Reader
    ↓
Column Filter                 (gerekli ham sütunlar)
    ↓
Rule Engine                   (item bayrakları üret: SM1_ON, SM2_ON, …)
    ↓
Column Filter                 (sadece item sütunları)
    ↓
Create Bit Vector             (veya: Collection / ItemSet hazırlığı)
    ↓
Association Rule Learner      (Apriori / FP-Growth — KNIME sürümüne göre ad)
    ↓
Association Rule Filter       (isteğe bağlı: min support/confidence)
    ↓
Table View / Rule Viewer
```

> Node adları KNIME sürümünde şöyle de görünebilir:  
> `Association Rule Learner (Borgelt)`, `Item Set Finder`, `Numeric Binner` + `Create Bit Vector`.

---

## Pratik minimum hat

```
CSV Reader
↓
Rule Engine          ← item’ları oluştur
↓
Column Filter        ← yalnız item’lar
↓
Create Bit Vector
↓
Association Rule Learner
↓
Table View
```

---

## 1. CSV Reader
| Ayar | Değer |
| --- | --- |
| File | `household_power_hourly.csv` |
| Delimiter | `,` |
| Header | ✓ |

---

## 2. Rule Engine — item üretimi

Çıktı sütunları (String veya Integer 0/1; Bit Vector için genelde boolean/0-1):

| Kural (örnek) | Item adı |
| --- | --- |
| `$Sub_metering_1$ > 0` | SM1_ON |
| `$Sub_metering_2$ > 0` | SM2_ON |
| `$Sub_metering_3$ > 0` | SM3_ON |
| `$Global_active_power$ > 2.0` | High_Load |
| `$Hour$ >= 18 AND $Hour$ <= 22` | Peak_Hour |
| `$IsWeekend$ = 1` | Weekend |

Dosyada `SM1_ON`, `SM2_ON`, `SM3_ON`, `High_Load`, `Peak_Hour`, `IsWeekend` **zaten varsa** Rule Engine atlanabilir; doğrudan Column Filter ile bunları seç.

---

## 3. Column Filter (item’lar)

**Include:** SM1_ON, SM2_ON, SM3_ON, High_Load, Peak_Hour, Weekend/IsWeekend  

**Exclude:** GAP, Voltage, Datetime, Consumption_Class, ham sürekli ölçümler

---

## 4. Create Bit Vector
- Seçilen item sütunlarından bit vektör / transaction formatı oluştur  
- “true / 1 / ON” → item mevcut

---

## 5. Association Rule Learner
| Ayar | Öneri (başlangıç) |
| --- | --- |
| Minimum support | **0.05 – 0.15** (veriye göre ayarla) |
| Minimum confidence | **0.4 – 0.6** |
| Max itemset length | 3–4 |

Çok az kural → support düşür.  
Çok fazla kural → support/confidence yükselt.

---

## 6. Sonuçları nasıl oku?
Her kural: **Antecedent → Consequent**  
- Support: ne sıklıkta birlikte  
- Confidence: A varken B olma oranı  
- Lift (>1 faydalı ilişki)

Örnek yorum çerçevesi:  
`Peak_Hour, SM3_ON → High_Load` (akşam + ısıtıcı/klima → yüksek yük)

---

## Cursor’dan node listesi

1. CSV Reader  
2. Column Filter *(veya Rule Engine + Column Filter)*  
3. Create Bit Vector  
4. Association Rule Learner  
5. Table View  
6. Association Rule Filter *(opsiyonel)*  

---

## KNIME’da senin adımların

1. New Workflow → **`04_Birliktelik_Enerji`**
2. Yukarıdaki sırayı kur  
3. Önce hazır bayrak sütunlarını dene (`SM*_ON`, `High_Load`, `Peak_Hour`, `IsWeekend`)  
4. Execute → kuralları Table View’da incele  
5. En anlamlı 3–5 kuralı not et / screenshot al  
6. Export → `knime/04_Birliktelik_Enerji.knwf`
