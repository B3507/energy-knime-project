# Anomali Tespiti Raporu
## Enerji Tüketimi — KNIME Analytics Platform

**Workflow:** `05_Anomali_Enerji`  
**Veri:** dakika/saatlik enerji ölçümleri (Numeric Outliers sonrası ~2.049.280 satır)  
**Yöntem:** Normalizer (Min-Max) + Numeric Outliers (IQR, k=1.5)  
**Tarih:** 26.08.2026  

---

## 1. Amaç

Normal elektrik tüketimi / gerilim / alt sayaç davranışından sapan gözlemleri (outlier) tespit etmek.

---

## 2. Node yapısı

```
CSV Reader → Column Filter → Normalizer → Numeric Outliers → Scatter Plot
```

| Ayar | Değer |
| --- | --- |
| Normalizer | Min-Max |
| Numeric Outliers | IQR, k = 1.5 |
| Analiz sütunları | Global_active_power, Voltage, Global_intensity, Sub_metering_1/2/3 |

---

## 3. Sonuçlar — sütun başına outlier sayısı

Kaynak: KNIME Numeric Outliers özet çıktısı · Scatter: X=`Outlier column`, Y=`Outlier count`

| Outlier column | Outlier count (yaklaşık) | Oran (~2.049.280 satıra) |
| --- | ---: | ---: |
| Global_active_power | ~95.000 | ~%4,6 |
| Voltage | ~50.000 | ~%2,4 |
| Global_intensity | ~100.000 | ~%4,9 |
| Sub_metering_1 | ~170.000 | ~%8,3 |
| Sub_metering_2 | ~75.000 | ~%3,7 |
| Sub_metering_3 | ~0 | ~%0 |

### Yorum
- En çok anomali **Sub_metering_1** (mutfak) ve **Global_intensity** / **Global_active_power** tarafında.  
- **Voltage** daha az outlier üretmiş (~50 bin).  
- **Sub_metering_3** neredeyse outlier üretmemiş — dağılım IQR’ye göre “daha düzenli” veya farklı karakterde.  
- Bu özet, satır satır GAP×Voltage scatter yerine **sütun bazlı anomali yoğunluğunu** gösterir; ödev için Numeric Outliers çıktısının doğrudan görselleştirmesidir.

---

## 4. Görseller

| Dosya | Durum |
| --- | --- |
| `screenshots/05_anomaly_outlier_counts.png` | Eklendi |
| `screenshots/05_anomaly_workflow.png` | İsteğe bağlı (tuval) |

---

## 5. Sonuç

IQR tabanlı Numeric Outliers ile enerji değişkenlerinde anomali sayıları elde edildi.  
En anomali yoğun sütun: **Sub_metering_1**; SM3 neredeyse temiz.

---

*Yalnızca anomali tespiti.*
