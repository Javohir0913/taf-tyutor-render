@echo off
chcp 65001 >nul
REM TAF-TYUTOR — lokal serverni ishga tushirish
cd /d "%~dp0"
call venv\Scripts\activate.bat

echo.
echo  Forma:        http://127.0.0.1:8000/
echo  Admin panel:  http://127.0.0.1:8000/admin/
echo  To'xtatish:   Ctrl+C
echo.
python manage.py runserver 127.0.0.1:8000
pause
