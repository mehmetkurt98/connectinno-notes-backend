@echo off
echo ========================================
echo Connectinno Backend Başlatılıyor...
echo ========================================

REM Backend klasörüne git
cd /d "%~dp0"

REM Virtual environment'ı aktifleştir
echo Virtual environment aktifleştiriliyor...
call .venv\Scripts\activate.bat

REM Python PATH'ini geçici olarak ekle
set PATH=%CD%\.venv\Scripts;%PATH%

REM Backend'i başlat
echo Backend sunucusu başlatılıyor...
echo URL: http://localhost:8000
echo.
python main.py

pause
