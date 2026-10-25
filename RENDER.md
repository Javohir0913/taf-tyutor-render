# TAF-TYUTOR — Render.com'ga joylashtirish

## 0. "config topilmadi" xatosining sababi

Render `manage.py` va `config/` papkasini **repo ildizidan** qidiradi. Repo shunday bo'lishi kerak:

```
(repo ildizi)
├── manage.py
├── config/
├── students/
├── requirements.txt
├── build.sh
├── start.sh
└── render.yaml
```

Agar GitHub'da hammasi `taf-tyutor/` papkasi ichida tursa, ikki yo'ldan birini tanlang:
- **A (oson):** Render'da **Settings > Build & Deploy > Root Directory** ga `taf-tyutor` yozing.
- **B:** fayllarni repo ildiziga ko'chiring va qayta push qiling.

## 1. Muhim: doimiy disk kerak

Render'da serverning o'z fayl tizimi har deploy va qayta ishga tushishda **tozalanadi**.
Disk ulanmasa, baza (`db.sqlite3`) va barcha **pasport nusxalari yo'qoladi**.
Doimiy disk (**Disks**) faqat pullik instance'larda ishlaydi (Starter va yuqori).
Bepul (Free) tarif faqat qisqa sinov uchun yaraydi.

## 2. Web Service yaratish

**Dashboard > New > Web Service** > GitHub repo'ni tanlang.

| Sozlama | Qiymat |
|---|---|
| Language | `Python 3` |
| Root Directory | bo'sh (yoki `taf-tyutor`, 0-bandga qarang) |
| Build Command | `./build.sh` |
| Start Command | `./start.sh` |
| Instance Type | `Starter` (disk uchun) |

## 3. Disk

**Advanced > Add Disk** (yoki keyinroq **Disks** bo'limida):

| Sozlama | Qiymat |
|---|---|
| Name | `data` |
| Mount Path | `/var/data` |
| Size | `1 GB` (taxminan 200+ ta pasport uchun yetadi) |

## 4. Environment Variables

**Environment > Add Environment Variable**:

| Key | Value |
|---|---|
| `PYTHON_VERSION` | `3.12.7` |
| `DEBUG` | `False` |
| `USE_HTTPS` | `True` |
| `SECRET_KEY` | **Generate** tugmasi bilan yarating |
| `SQLITE_PATH` | `/var/data/db.sqlite3` |
| `PRIVATE_MEDIA_ROOT` | `/var/data/private_media` |
| `DJANGO_SUPERUSER_USERNAME` | admin logini, masalan `java` |
| `DJANGO_SUPERUSER_PASSWORD` | **kamida 10 belgili kuchli parol** |

`ALLOWED_HOSTS` va `CSRF_TRUSTED_ORIGINS` shart emas: `*.onrender.com` domeni avtomatik qo'shiladi.
O'z domeningizni ulasangiz: `ALLOWED_HOSTS=tyutor.example.uz`, `CSRF_TRUSTED_ORIGINS=https://tyutor.example.uz`.

## 5. Deploy

**Create Web Service** (yoki **Manual Deploy > Deploy latest commit**).
**Logs** bo'limida quyidagilar chiqishi kerak:

```
... static files copied ...
Applying students.0001_initial... OK
Admin yaratildi: java
Listening at: http://0.0.0.0:10000
```

Keyin `https://<nom>.onrender.com/admin/` ga kiring va **Guruhlar > + Add** orqali guruhlarni qo'shing.

Admin bir marta yaratilgach, `DJANGO_SUPERUSER_PASSWORD` ni Environment'dan o'chirib qo'yish mumkin.
Parolni keyin almashtirish: admin panelda **Change password** (yuqori o'ng burchak).

## Tez-tez uchraydigan xatolar

| Logdagi xato | Sabab va yechim |
|---|---|
| `ModuleNotFoundError: No module named 'config'` | 0-band: Root Directory noto'g'ri |
| `./build.sh: Permission denied` | Build Command'ni `bash build.sh`, Start Command'ni `bash start.sh` qiling |
| `RuntimeError: SECRET_KEY ... berilmagan` | 4-band: `SECRET_KEY` qo'shilmagan |
| `DisallowedHost` | o'z domeningiz `ALLOWED_HOSTS` ga yozilmagan |
| `unable to open database file` | disk ulanmagan yoki Mount Path `/var/data` emas |
| Admin'ga kirganda `403 CSRF` | o'z domeningiz `CSRF_TRUSTED_ORIGINS` ga `https://` bilan yozilmagan |
