# KNIME Veri Ön İşleme Planı
# Kaynak: data/household_power_consumption.txt
# Kapsam: Yalnızca veri hazırlama — ML Learner yok

## Ortak hat (önerilen)

CSV Reader
↓
String to Number
↓
Missing Value
↓
String to Date&Time  (Date)
↓
String to Date&Time  (Time)
↓
Create Date&Time Column
↓
Extract Date&Time Fields
↓
Rule Engine  (is_weekend vb.)
↓
Numeric Outliers  (işaretle, silme)
↓
Column Filter
↓
(isteğe bağlı) Date&Time Round → GroupBy  [saatlik]
↓
─── dallar ───
  Kümeleme:        Column Filter → Normalizer
  Regresyon:       Column Filter (Intensity OUT)
  Sınıflandırma:   Rule Engine (Low/Med/High) → Column Filter
  Birliktelik:     Rule Engine (ON bayrakları) → Column Filter → Create Bit Vector
  Anomali:         Column Filter → Normalizer → Numeric Outliers

## CSV Reader ayarları
- Delimiter: ;
- Has Column Header: true
- Missing Value Pattern: ?
- Encoding: UTF-8

## Date / Time
- Date format: dd/MM/yyyy
- Time format: HH:mm:ss
- Extract: Year, Month, Day, Hour, Minute, Day of week

## Eksik değer
- Remove row (25.979 satır, %1.25) — önerilen

## Regresyon hedefi
- Global_active_power
- Global_intensity KULLANMA (hedef sızıntısı)

## Sınıflandırma (Rule Engine örneği)
- <= 0.5 → Low
- <= 2.0 → Medium
- else → High

## Association items
- SM1_ON, SM2_ON, SM3_ON, High_Load, Peak_Hour, Weekend
