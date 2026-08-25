# knime/

Bu klasörde KNIME Analytics Platform üzerinde oluşturulan workflow dosyaları saklanır.

## Önemli
- Workflow'lar **Cursor'da kod olarak yazılmaz**.
- KNIME Analytics Platform GUI'de kurulur.
- Buraya kaydedilecekler (KNIME'dan export/save):
  - `*.knwf` / `*.knar` workflow dosyaları
  - isteğe bağlı node ayar notları

## KNIME'da okunacak veri
Önerilen (küçük, temiz):
`../data/household_power_hourly.csv`

Dakika çözünürlüğü (büyük):
`../data/household_power_clean.csv`

CSV ayarları: delimiter = `,` · header = yes · encoding = UTF-8
