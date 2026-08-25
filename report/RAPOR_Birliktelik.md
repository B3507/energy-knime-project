# Birliktelik Kuralı Raporu
## Enerji Tüketimi — KNIME Analytics Platform

**Workflow:** `04_Birliktelik_Enerji`  
**Yöntem:** Create Bit Vector (Multiple numeric) + Association Rule Learner  
**Tarih:** 25.08.2026  

---

## 1. Amaç

Aynı zaman diliminde birlikte görülen enerji durumlarını keşfetmek.

---

## 2. Item'lar

| Item | Anlam |
| --- | --- |
| SM1_ON | Mutfak aktif |
| SM2_ON | Çamaşır / yıkama aktif |
| SM3_ON | Isıtıcı / klima aktif |
| High_Load | Yüksek aktif güç |
| Peak_Hour | Pik saat |
| IsWeekend | Hafta sonu |

---

## 3. Node yapısı

```
CSV Reader → Column Filter → Create Bit Vector → Association Rule Learner → Table View
```

| Ayar | Değer |
| --- | --- |
| Bit Vector | Multiple numeric (0/1 bayraklar) |
| Min support | 0.05 |
| Output association rules | Açık |
| Max itemset length | 4 |

> Consumption_Class + Bit string kullanılmamalı.

---

## 4. Sonuçlar

### Sık itemset (Support)

| Support | Items | Yorum |
| ---: | --- | --- |
| 0,584 | SM3_ON | En sık (~%58) |
| 0,145 | SM2_ON, SM3_ON | İki sayaç birlikte |
| 0,121 | High_Load, SM3_ON | Yüksek yük + SM3 |
| 0,114 | Peak_Hour, SM3_ON | Pik + SM3 |
| 0,062 | High_Load, SM2_ON | Yüksek yük + SM2 |

### Rules çıktısı (21 satır)

KNIME `rule0`…`rule20` üretti; format tek sütun Items (Collection). Ayrı Confidence sütunu bu çıktıda yok.

Öne çıkan birliktelikler: High_Load+SM3_ON, High_Load+SM2_ON, High_Load+Peak_Hour, SM3_ON+Peak_Hour, SM2_ON+SM3_ON.

### Yorum

Yüksek tüketim; SM2/SM3 aktivitesi ve pik saat ile birlikte görünüyor. SM3_ON tek başına en sık item.

---

## 5. Görseller

| Dosya | Durum |
| --- | --- |
| `screenshots/04_association_workflow.png` | Tamam |
| `screenshots/04_association_itemsets.png` | Tamam |
| `screenshots/04_association_rules.png` | Tamam |

Word: `report/RAPOR_Birliktelik.docx`

---

## 6. Sonuç

Birliktelik workflow'u tamamlandı. Support'lu itemset ve rule etiketli kümeler belgelendi. Confidence sütunu bu KNIME çıktı formatında üretilmedi.

---

*Yalnızca birliktelik.*
