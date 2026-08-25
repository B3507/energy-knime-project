# 03_Classification — Şimdi yapılacaklar

Workflow: **03_Siniflandirma_Enerji**  
Veri: `data/household_power_hourly.csv`

## Node yapısı

```
CSV Reader → Column Filter → Partitioning
                    Train → Decision Tree Learner
                    Test + model → Decision Tree Predictor
                                 → Scorer
```

## Column Filter
**Include:** Consumption_Class, reactive, Voltage, SM1, SM2, SM3, Hour, DayOfWeek, Month  
**Exclude:** Global_active_power, Global_intensity, High_Load, Peak_Hour, SM*_ON (önerilen)

## Hedef
`Consumption_Class` = Low / Medium / High

## Sonra
Scorer Accuracy + Confusion Matrix → `screenshots/03_classification_*.png`  
Rapor: `report/RAPOR_Siniflandirma.md`
