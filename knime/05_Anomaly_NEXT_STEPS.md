# 05_Anomaly — Şimdi yapılacaklar

Workflow: **05_Anomali_Enerji**  
Veri: `data/household_power_hourly.csv`

## Node yapısı

```
CSV Reader → Column Filter → Normalizer → Numeric Outliers → Scatter Plot
```

## Column Filter
Include: Global_active_power, Voltage, Global_intensity, Sub_metering_1/2/3  
Exclude: Consumption_Class, SM*_ON, High_Load, Peak_Hour (zorunlu değil)

## Numeric Outliers
Method: IQR · GAP + Voltage (en az)

## Sonra
Anomali sayısı + oran + Scatter screenshot → `report/RAPOR_Anomali.md`
