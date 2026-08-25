# Proje sanal ortamini aktif et (PowerShell)
# Kullanim: .\activate.ps1
Set-Location $PSScriptRoot
& "$PSScriptRoot\.venv\Scripts\Activate.ps1"
Write-Host "Aktif: $env:VIRTUAL_ENV"
python --version
