# 04_Association — Şimdi yapılacaklar

Workflow: **04_Birliktelik_Enerji**  
Veri: `data/household_power_hourly.csv`

## Node yapısı

```
CSV Reader
↓
Column Filter          ← SM1_ON, SM2_ON, SM3_ON, High_Load, Peak_Hour, IsWeekend
↓
Create Bit Vector
↓
Association Rule Learner
↓
Table View
```

Bayraklar yoksa önce **Rule Engine** ile üret (plan dosyasına bak).

## Ayar başlangıcı
- Min support: 0.10  
- Min confidence: 0.50  

## Sonra
Anlamlı kuralları screenshot + `report/RAPOR_Birliktelik.md`
