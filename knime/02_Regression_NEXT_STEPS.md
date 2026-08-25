# 02_Regression — Şimdi yapılacaklar

Workflow adı: **02_Regression**  
Veri: `data/household_power_hourly.csv`

## Şimdi KNIME’de (sırayla)

1. File → New → New KNIME Workflow → `02_Regression`
2. **CSV Reader** ekle → dosya yolu hourly CSV → delimiter `,` → Execute
3. **Column Filter** → Include: GAP, reactive, Voltage, SM1, SM2, SM3, Hour, DayOfWeek, Month  
   Exclude: Intensity, Class, SM*_ON, High_Load, Peak_Hour, Datetime…
4. **Normalizer** (Min-Max) → **Global_active_power’ı normalize etme**
5. **Partitioning** → 70/30, seed 42
6. Train → **Linear Regression Learner** (target = Global_active_power)
7. Model + Test → **Regression Predictor**
8. **Numeric Scorer** → R², MAE, RMSE not et
9. **Scatter Plot** (gerçek vs tahmin) → screenshot

## Bağlantı

```
CSV Reader → Column Filter → Normalizer → Partitioning
                                      ╱          ╲
                                   Train         Test
                                     ↓             ↓
                          Linear Regression    (data)
                               Learner ──model──► Regression Predictor
                                                       ↓
                                                 Numeric Scorer
                                                       ↓
                                                  Scatter Plot
```

## Kaydet

- Screenshot → `screenshots/02_regression_*.png`
- Workflow export → `knime/02_Regression.knwf`
- Skorlar → `report/RAPOR_Regresyon.md`
