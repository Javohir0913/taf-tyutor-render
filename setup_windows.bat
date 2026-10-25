@echo off
chcp 65001 >nul
REM TAF-TYUTOR — Windows'da birinchi marta o'rnatish
cd /d "%~dp0"

echo [1/5] Virtual muhit yaratilmoqda...
if not exist venv (
    python -m venv venv || (echo Python topilmadi. python.org dan Python 3.12 o'rnating va "Add to PATH" ni belgilang. & pause & exit /b 1)
)

echo [2/5] Kutubxonalar o'rnatilmoqda...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
pip install -r requirements.txt || (echo Kutubxonalarni o'rnatib bo'lmadi. Internetni tekshiring. & pause & exit /b 1)

echo [3/5] .env fayli tayyorlanmoqda...
if not exist .env (
    copy .env.example .env >nul
    python -c "import secrets,re,io;p='.env';s=open(p,encoding='utf-8').read();s=re.sub(r'(?m)^SECRET_KEY=.*$','SECRET_KEY='+secrets.token_urlsafe(50),s);open(p,'w',encoding='utf-8').write(s)"
)

echo [4/5] Ma'lumotlar bazasi yaratilmoqda...
python manage.py migrate || (pause & exit /b 1)

echo [5/5] Admin foydalanuvchi yaratiladi (login va parol kiriting):
python manage.py createsuperuser

echo.
echo Tayyor! Endi start_windows.bat ni ishga tushiring.
pause
