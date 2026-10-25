#!/usr/bin/env bash
# Kod yangilangandan keyin ishga tushiriladi (taftyutor foydalanuvchisi nomidan emas, sudo bilan):
#   sudo /srv/taf-tyutor/deploy/update.sh
set -euo pipefail
cd /srv/taf-tyutor

sudo -u taftyutor venv/bin/pip install -q -r requirements.txt
sudo -u taftyutor venv/bin/python manage.py migrate --noinput
sudo -u taftyutor venv/bin/python manage.py collectstatic --noinput -v0
sudo -u taftyutor venv/bin/python manage.py check --deploy --fail-level ERROR

systemctl restart taf-tyutor
systemctl --no-pager --lines=0 status taf-tyutor
echo "Yangilandi."
