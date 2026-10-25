# TAF-TYUTOR — serverga joylashtirish (Ubuntu 22.04 / 24.04)

Sxema: **Internet → Nginx (80/443) → Gunicorn (unix socket) → Django → SQLite**

Quyida `DOMEN_NOMI` — sizning domeningiz (masalan `tyutor.example.uz`),
`SERVER_IP` — serverning tashqi IP manzili. Barcha buyruqlar serverda, `sudo` huquqli foydalanuvchi nomidan.

---

## 1. Serverni tayyorlash

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip nginx sqlite3 unzip
sudo ufw allow OpenSSH
sudo ufw allow "Nginx Full"
sudo ufw enable
```

## 2. Alohida foydalanuvchi va papka

Sayt root nomidan emas, o'zining cheklangan foydalanuvchisi nomidan ishlaydi.

```bash
sudo adduser --system --group --home /srv/taf-tyutor taftyutor
```

Kompyuteringizdan arxivni serverga yuboring (Windows PowerShell'da):

```powershell
scp taf-tyutor.zip USER@SERVER_IP:/tmp/
```

Serverda oching:

```bash
cd /tmp && unzip -o taf-tyutor.zip
sudo cp -a /tmp/taf-tyutor/. /srv/taf-tyutor/
sudo chown -R taftyutor:www-data /srv/taf-tyutor
sudo chmod 750 /srv/taf-tyutor
sudo chmod +x /srv/taf-tyutor/deploy/*.sh
```

## 3. Python muhiti

```bash
cd /srv/taf-tyutor
sudo -u taftyutor python3 -m venv venv
sudo -u taftyutor venv/bin/pip install -r requirements.txt
```

## 4. `.env` sozlamalari

```bash
sudo -u taftyutor cp .env.example .env
sudo -u taftyutor venv/bin/python -c "import secrets; print(secrets.token_urlsafe(50))"
sudo -u taftyutor nano .env
```

Domen bilan:

```
DEBUG=False
SECRET_KEY=<yuqorida chiqqan kalit>
ALLOWED_HOSTS=DOMEN_NOMI
CSRF_TRUSTED_ORIGINS=https://DOMEN_NOMI
USE_HTTPS=True
PRIVATE_MEDIA_ROOT=
```

Domen hali yo'q, vaqtincha IP orqali:

```
DEBUG=False
SECRET_KEY=<yuqorida chiqqan kalit>
ALLOWED_HOSTS=SERVER_IP
CSRF_TRUSTED_ORIGINS=http://SERVER_IP
USE_HTTPS=False
```

Saqlash: `Ctrl+O`, `Enter`, `Ctrl+X`. Keyin:

```bash
sudo chmod 600 /srv/taf-tyutor/.env
```

## 5. Baza, statik fayllar, admin

```bash
cd /srv/taf-tyutor
sudo -u taftyutor venv/bin/python manage.py migrate
sudo -u taftyutor venv/bin/python manage.py collectstatic --noinput
sudo -u taftyutor venv/bin/python manage.py createsuperuser
sudo -u taftyutor mkdir -p private_media
sudo chmod 700 /srv/taf-tyutor/private_media
```

**Lokal kompyuterdagi ma'lumotlarni ko'chirish** (agar kerak bo'lsa) — `migrate` dan OLDIN:

```powershell
scp db.sqlite3 USER@SERVER_IP:/tmp/
scp -r private_media USER@SERVER_IP:/tmp/
```

```bash
sudo cp /tmp/db.sqlite3 /srv/taf-tyutor/
sudo cp -r /tmp/private_media /srv/taf-tyutor/
sudo chown -R taftyutor:www-data /srv/taf-tyutor/db.sqlite3 /srv/taf-tyutor/private_media
sudo chmod 700 /srv/taf-tyutor/private_media
```

Bu holda `createsuperuser` shart emas — lokal admin ham ko'chadi.
**Lokaldagi `java/java` paroli bilan qoldirmang:**
`sudo -u taftyutor venv/bin/python manage.py changepassword java`

## 6. Gunicorn xizmati

```bash
sudo cp /srv/taf-tyutor/deploy/taf-tyutor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now taf-tyutor
sudo systemctl status taf-tyutor
```

`active (running)` yozuvi chiqishi kerak. Xato bo'lsa: `sudo journalctl -u taf-tyutor -n 50`

## 7. Nginx

```bash
sudo cp /srv/taf-tyutor/deploy/nginx-taf-tyutor.conf /etc/nginx/sites-available/taf-tyutor
sudo sed -i 's/DOMEN_NOMI/tyutor.example.uz/' /etc/nginx/sites-available/taf-tyutor   # domen yoki SERVER_IP
sudo ln -s /etc/nginx/sites-available/taf-tyutor /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

`nginx -t` — `syntax is ok` va `test is successful` chiqishi shart.

## 8. HTTPS (domen bo'lsa)

1. DNS'da `A` yozuv: `DOMEN_NOMI → SERVER_IP` (Cloudflare bo'lsa, avval **Proxy status: DNS only** qiling).
2. Sertifikat:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d DOMEN_NOMI --redirect
```

Sertifikat 90 kunda o'zi yangilanadi. Tekshirish: `sudo certbot renew --dry-run`

## 9. Kunlik zaxira

```bash
sudo crontab -e
```

Oxiriga qo'shing:

```
15 2 * * * /srv/taf-tyutor/deploy/backup.sh >> /var/log/taf-tyutor-backup.log 2>&1
```

Zaxiralar: `/var/backups/taf-tyutor/` (14 kun saqlanadi). Imkon bo'lsa, ularni boshqa diskka/serverga ham nusxalang.

## 10. Tekshirish

- `https://DOMEN_NOMI/` — forma ochiladi
- `https://DOMEN_NOMI/admin/` — kirish ishlaydi, guruh qo'shiladi
- Telefondan forma to'ldiring, pasport yuklang → admin'da **Ko'rish** ochiladi
- Login qilmagan brauzerda `/passport/1/` → login sahifasiga qaytarishi kerak

## Kodni keyinchalik yangilash

Yangi fayllarni `/srv/taf-tyutor/` ga ko'chirgach (`.env`, `db.sqlite3`, `private_media/` ga tegmang):

```bash
sudo chown -R taftyutor:www-data /srv/taf-tyutor
sudo /srv/taf-tyutor/deploy/update.sh
```
