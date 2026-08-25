# 01_Clustering — Kalan adımlar (node’lar kurulduktan sonra)

KNIME’da node’lar bağlandı. Bundan sonra yapılacaklar:

---

## A. Ayar kontrol listesi (Execute öncesi)

### 1. CSV Reader
- [ ] Dosya: `data/household_power_hourly.csv`
- [ ] Delimiter: `,`
- [ ] Has Column Header: ✓
- [ ] Encoding: UTF-8

### 2. Column Filter — INCLUDE
- [ ] Global_active_power
- [ ] Global_reactive_power
- [ ] Voltage
- [ ] Sub_metering_1
- [ ] Sub_metering_2
- [ ] Sub_metering_3
- [ ] (opsiyonel) Hour

### 2b. Column Filter — EXCLUDE
- [ ] Global_intensity
- [ ] Consumption_Class, SM1_ON, SM2_ON, SM3_ON, High_Load, Peak_Hour
- [ ] Datetime / Year / Month / Day / Minute (özellik olarak değil)

### 3. Normalizer
- [ ] Method: Min-Max (0–1)
- [ ] Tüm seçili sayısal sütunlar işaretli

### 4. k-Means
- [ ] Number of clusters **k = 3** (ilk deneme)
- [ ] Max iterations: 100
- [ ] Random seed: **42** (tekrarlanabilirlik)

### 5. Color Manager
- [ ] Color column = Cluster (veya k-Means’in ürettiği etiket sütunu)

### 6. Scatter Plot
- [ ] X: Global_active_power (veya normalize hali)
- [ ] Y: Sub_metering_3 veya Voltage
- [ ] Color: Cluster

---

## B. İlk çalıştırma

1. Workflow’da **Reset** (gerekirse) → **Execute all** (Shift+F7 veya yeşil çift ok)
2. Her node yeşil tik olmalı; kırmızı = hata → o node’un log’una bak
3. k-Means çıktısını **Table View** ile aç:
   - Yeni sütun: `Cluster` (0, 1, 2 …)
   - Satır sayısı ≈ 34.168 (saatlik dosya)

**Screenshot:** `screenshots/01_clustering_workflow.png` (tüm hat)  
**Screenshot:** `screenshots/01_clustering_table_k3.png` (cluster sütunu)

---

## C. Cluster sayısını değerlendirme (zorunlu)

Aynı workflow’da **k** değerini değiştirip tekrar çalıştır:

| Deneme | k | Ne kaydedeceksin |
| --- | --- | --- |
| 1 | 2 | Silhouette skoru + küme boyutları |
| 2 | 3 | Silhouette skoru + küme boyutları |
| 3 | 4 | Silhouette skoru + küme boyutları |
| 4 | 5 | Silhouette skoru + küme boyutları |

### Silhouette Coefficient
- Giriş: normalize özellikler + Cluster etiketi
- Her k için skoru not et (0’a yakın kötü, 1’e yakın iyi — pratikte 0.2–0.6 arası sık görülür)
- **En iyi (veya dengeli boyut + iyi skor) k’yı seç** → asıl sonuç bu k ile

Küme boyutları için:
```
k-Means → GroupBy (Group = Cluster, Aggregation = Count / Mean)
```
veya Pie / Bar Chart.

**Screenshot:** `screenshots/01_clustering_silhouette_k2_to_k5.png`  
**Screenshot:** `screenshots/01_clustering_sizes_best_k.png`

Rapor tablosu (sen dolduracaksın):

| k | Silhouette | Küme boyutları (n) | Not |
| --- | --- | --- | --- |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |
| **Seçilen** |  |  |  |

---

## D. Görselleştirme (seçilen k ile)

1. **Scatter Plot** — kümelerin ayrışması  
   → `screenshots/01_clustering_scatter.png`
2. **Conditional Box Plot** — Cluster vs Global_active_power  
   → `screenshots/01_clustering_boxplot.png`
3. **Pie / Bar Chart** — küme oranları  
   → `screenshots/01_clustering_pie.png`
4. **GroupBy** — Cluster başına Mean(GAP, Voltage, SM1, SM2, SM3)  
   → `screenshots/01_clustering_profiles.png`

---

## E. Sonuçları enerji diliyle yorumla (sen yazacaksın)

Model sonucunu Cursor tahmin etmez. Table/GroupBy’a bakıp şunu doldur:

| Cluster | Ortalama GAP | SM1/SM2/SM3 | Olası anlam (örnek çerçeve) |
| --- | --- | --- | --- |
| 0 | … | … | Düşük yük / gece? |
| 1 | … | … | Orta kullanım? |
| 2 | … | … | Yüksek yük / ısıtıcı? |

Kurallar:
- En düşük ortalama `Global_active_power` → düşük tüketim profili
- Yüksek `Sub_metering_3` → ısıtıcı/klima ağırlıklı saatler
- Yüksek SM1 → mutfak aktivitesi

---

## F. Kaydetme

1. Workflow kaydet: **`01_Clustering`**
2. Export/kopyala → `knime/01_Clustering.knwf` (veya KNIME workspace kopyası)
3. Tüm ekran görüntüleri → `screenshots/`
4. Kısa not → `report/01_clustering_notes.md` (k seçimi + 2–3 cümle yorum)

---

## G. Bitti sayılır mı?

- [ ] Workflow hatasız execute
- [ ] k=2..5 karşılaştırıldı, k seçildi
- [ ] Scatter + box + boyut görselleri alındı
- [ ] Küme profilleri (GroupBy) yorumlandı
- [ ] `knime/` + `screenshots/` güncel

Sonraki ML problemi (Cursor’a söyle): **02_Regression**
