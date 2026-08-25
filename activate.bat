@echo off
cd /d "%~dp0"
call "%~dp0.venv\Scripts\activate.bat"
echo Aktif: %VIRTUAL_ENV%
python --version
