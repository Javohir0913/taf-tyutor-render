#!/usr/bin/env bash
# Kunlik zaxira: baza + pasportlar + .env. 14 kundan eskilari o'chiriladi.
# cron:  15 2 * * *  /srv/taf-tyutor/deploy/backup.sh
set -euo pipefail

APP=/srv/taf-tyutor
DEST=/var/backups/taf-tyutor
STAMP=$(date +%Y-%m-%d_%H-%M)
mkdir -p "$DEST"
chmod 700 "$DEST"

# SQLite'ni ishlab turgan holatda xavfsiz nusxalash
sqlite3 "$APP/db.sqlite3" ".backup '$DEST/db_$STAMP.sqlite3'"

tar -czf "$DEST/files_$STAMP.tar.gz" -C "$APP" private_media .env

find "$DEST" -type f -mtime +14 -delete
echo "Zaxira tayyor: $DEST ($STAMP)"
