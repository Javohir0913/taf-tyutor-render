# TAF-TYUTOR — talabalar ro'yxati

Talaba ro'yxatdan o'tadi (kurs, guruh, F.I.Sh., yashash joyi, manzil, xaritada uy — ixtiyoriy, pasport nusxasi).
Tyutor admin panelda ko'radi, filtrlaydi, pasportni ochadi, Excelga yuklab oladi.

## Windows'da lokal ishga tushirish

1. Python 3.12 o'rnating (python.org), o'rnatishda **"Add python.exe to PATH"** ni belgilang.
2. `setup_windows.bat` ni ikki marta bosing — bir marta, birinchi safar.
   Oxirida admin login, email (bo'sh qoldirsa bo'ladi) va parol so'raladi.
3. `start_windows.bat` ni ikki marta bosing.
4. Brauzerda:
   - Forma: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

Birinchi ish: Admin → **Guruhlar → + Add** orqali guruhlarni kiriting, aks holda formada guruh chiqmaydi.

## Muhim fayllar (Git'ga qo'shilmaydi)

- `.env` — maxfiy kalit va sozlamalar
- `db.sqlite3` — ma'lumotlar bazasi
- `private_media/` — pasport nusxalari

Bu uchtasini zaxiralab turing. Serverga ko'chirishda ham shu uchtasi ko'chiriladi.
