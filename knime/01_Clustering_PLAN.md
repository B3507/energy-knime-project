# 01_Clustering — KNIME Workflow Tasarımı

**Problem:** Kümeleme (unsupervised)  
**Veri:** `data/household_power_hourly.csv` (önerilen)  
**KNIME workflow adı:** `01_Clustering`  
**Kapsam:** Node listesi, sıra, ayarlar — model sonucunu tahmin etmez.

---

## Ana node zinciri (kesin sıra)

```
CSV Reader
↓
Column Filter
↓
Normalizer
↓
Numeric Outliers          (isteğe bağlı — sadece inceleme)
↓
k-Means
↓
Cluster Assigner          (çoğu k-Means sürümünde çıktıda cluster zaten gelir;
                          yoksa / ayrı node varsa buraya)
↓
Color Manager
↓
Scatter Plot
↓
(Parallel) Silhouette Coefficient   ← Normalizer çıktısından da bağlanabilir
↓
(Parallel) Conditional Box Plot
↓
(Parallel) Pie / Bar Chart (cluster boyutları)
```

**Pratik minimum hat (ödev için yeterli):**

```
CSV Reader
↓
Column Filter
↓
Normalizer
↓
k-Means
↓
Color Manager
↓
Scatter Plot
```

Değerlendirme ve ek görseller için aynı `k-Means` (veya Normalizer) çıktısından paralel dallar aç.

---

## 1. Kullanılacak KNIME node’ları

| Sıra | Node | Amaç |
| --- | --- | --- |
| 1 | **CSV Reader** | Temiz saatlik veriyi oku |
| 2 | **Column Filter** | Kümelemeye girecek sütunları seç |
| 3 | **Normalizer** | Farklı birimleri ölçekle |
| 4 | **k-Means** | Kümeleme modeli |
| 5 | **Color Manager** | Cluster’a renk |
| 6 | **Scatter Plot** | 2D görselleştirme |
| 7 | **Silhouette Coefficient** | k kalitesi (değerlendirme) |
| 8 | **Conditional Box Plot** | Küme bazlı dağılım |
| 9 | **Pie Chart** veya **Bar Chart** | Küme büyüklükleri |
| 10 | **GroupBy** (opsiyonel) | Cluster başına ortalama profil |
| 11 | **Numeric Outliers** (opsiyonel) | Aşırı uçları görmek (silmeden) |

> Not: KNIME sürümüne göre node adı `k-Means` / `kMeans` olabilir. Analytics Platform Node Repository’de **Mining → Clustering → k-Means** yolundan bulunur.

---

## 2. Node bağlantı sırası (detay)

```
[CSV Reader]
     |
     v
[Column Filter] --------------------+
     |                              |
     v                              |  (istersen ham sütunları
[Normalizer]                        |   GroupBy / Box Plot için sakla)
     |                              |
     +----------+-------------------+
     |          |
     v          v
 [k-Means]   [Silhouette Coefficient]  ← özellik = normalize edilmiş sütunlar
     |          (k denemelerinde ayrı çalıştır)
     |
     +----------+-------------------+
     |          |                   |
     v          v                   v
[Color Manager] [Conditional Box Plot] [GroupBy]
     |
     v
[Scatter Plot]
     |
     v
[Pie Chart / Bar Chart]
```

Kaydet: `knime/01_Clustering.knwf` (KNIME File → Export / Save As).

---

## 3. Her node’un ayarları

### 3.1 CSV Reader
| Ayar | Değer |
| --- | --- |
| File | `.../energy-knime-project/data/household_power_hourly.csv` |
| Has Column Header | ✓ |
| Delimiter / Column delimiter | `,` (virgül) |
| Encoding | UTF-8 |
| Missing Value Pattern | (gerekmez — temiz dosyada `?` yok) |

### 3.2 Column Filter
**Include (kümeleme özellikleri):**
- `Global_active_power`
- `Global_reactive_power`
- `Voltage`
- `Sub_metering_1`
- `Sub_metering_2`
- `Sub_metering_3`
- (isteğe bağlı) `Hour`

**Exclude:**
- `Datetime`, `Date`, `Time`, `Year`, `Month`, `Day`, `Minute`, `DayOfWeek`
- `Global_intensity` (GAP ile çok ilişkili — kümelemeyi bozabilir)
- `Consumption_Class`, `SM1_ON`, `SM2_ON`, `SM3_ON`, `High_Load`, `Peak_Hour`, `IsWeekend`  
  (bunlar etiket/bayrak; kümeleme girişine koyma — istersen sonra yorum için Join ile geri ekle)

### 3.3 Normalizer
| Ayar | Değer |
| --- | --- |
| Normalization method | **Min-Max** (0–1) — ödev için net ve görsel |
| Alternatif | Z-Score (mean=0, std=1) |
| Columns | Column Filter’daki tüm sayısal özellikler |

**Normalizasyon gerekli mi?** → **Evet.**  
Neden: kW, V, Wh birimleri farklı; k-Means Öklid mesafesi kullanır.

### 3.4 k-Means
| Ayar | Değer |
| --- | --- |
| Number of clusters (**k**) | **Başlangıç: 3** |
| Max number of iterations | 100 (varsayılan yeterli) |
| Random seed | Sabit seç (örn. **42**) — tekrarlanabilirlik |
| Columns | Normalize edilmiş özellikler (hepsi) |

### 3.5 Color Manager
- Color column: `Cluster` (veya k-Means’in ürettiği cluster sütunu)
- Nominal colors — her küme ayrı renk

### 3.6 Scatter Plot
| Ayar | Öneri |
| --- | --- |
| X axis | `Global_active_power` (normalize veya orijinal — Join ile orijinal tercih) |
| Y axis | `Sub_metering_3` veya `Voltage` |
| Color | Cluster |

Daha iyi: Normalizer öncesi sütunları **Joiner** ile cluster etiketine geri bağla, scatter’da orijinal birimlerde çiz.

### 3.7 Silhouette Coefficient
- Input: normalize edilmiş özellikler + Cluster etiketi
- Farklı **k = 2, 3, 4, 5** için workflow’u yeniden çalıştırıp skorları not et
- En iyi silhouette’e yakın k’yı seç (raporda tablo)

### 3.8 Conditional Box Plot
- Category: `Cluster`
- Numeric: `Global_active_power` (orijinal, Join sonrası)

### 3.9 GroupBy (opsiyonel profil tablosu)
- Group column: `Cluster`
- Aggregation: Mean of tüm özellikler
- Çıktı: her kümenin “enerji profili”

### 3.10 Pie / Bar Chart
- Cluster frekansları (kaç saat / satır hangi kümede)

---

## 4. Kullanılacak sütunlar (özet)

| Rol | Sütunlar |
| --- | --- |
| **Kümeleme özellikleri** | Global_active_power, Global_reactive_power, Voltage, Sub_metering_1, Sub_metering_2, Sub_metering_3 [, Hour] |
| **Kesinlikle çıkarılan** | Global_intensity, Consumption_Class, SM*_ON, High_Load, Peak_Hour, ham Date/Time string |
| **Görsel / yorum (Join sonrası)** | Datetime, Hour, Consumption_Class (küme anlamı yorumlamak için) |

---

## 5. Normalizasyon
**Evet — zorunlu.** Node: **Normalizer** (Min-Max önerilir).

---

## 6. Başlangıç k değeri
**k = 3**

Gerekçe (hipotez, sonuç değil): düşük / orta / yüksek tüketim profilleri için doğal bir başlangıç. Kesin sayı Silhouette ile seçilecek.

---

## 7. Cluster sayısının değerlendirilmesi
1. **Silhouette Coefficient** node → k = 2, 3, 4, 5 dene  
2. İsteğe bağlı: **k-Means** + manuel karşılaştırma (küme boyutları dengeli mi?)  
3. Rapor: her k için silhouette + küme boyut tablosu → seçilen k’yı gerekçelendir  

Elbow için KNIME’de hazır node her sürümde olmayabilir; ödev için Silhouette + görsel yeter.

---

## 8. Sonuçların görselleştirilmesi
| Node | Ne gösterir |
| --- | --- |
| Scatter Plot | 2 özellik düzleminde kümeler |
| Conditional Box Plot | Küme başına GAP dağılımı |
| Pie / Bar Chart | Küme büyüklükleri |
| GroupBy + Table View | Küme merkezleri / ortalama profiller |
| Color Manager | Tüm görsellerde tutarlı renk |

Ekran görüntülerini `screenshots/` altına kaydet (örn. `01_clustering_kmeans.png`).

---

## Cursor’dan gelen node listesi (kopyala-yapıştır)

1. CSV Reader  
2. Column Filter  
3. Normalizer  
4. k-Means  
5. Color Manager  
6. Scatter Plot  
7. Silhouette Coefficient  
8. Conditional Box Plot  
9. Pie Chart (veya Bar Chart)  
10. GroupBy *(opsiyonel)*  
11. Joiner *(opsiyonel — orijinal birimlerle görselleştirme)*  
12. Numeric Outliers *(opsiyonel)*  

**Minimum kurulum sırası:**  
`CSV Reader → Column Filter → Normalizer → k-Means → Color Manager → Scatter Plot`

---

## KNIME’da yapman gerekenler (sen)

1. KNIME Analytics Platform’u aç  
2. New Workflow → adı: **`01_Clustering`**  
3. Yukarıdaki sırayla node’ları ekle ve bağla  
4. `household_power_hourly.csv` yolunu CSV Reader’a ver  
5. k=3 ile Execute  
6. Silhouette için k=2…5 dene, screenshot al  
7. Workflow’u kaydet / export → `knime/01_Clustering.knwf`
