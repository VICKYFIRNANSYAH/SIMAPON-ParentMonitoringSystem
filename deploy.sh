#!/bin/bash
# Auto-deploy script untuk SIMAPON
# Dipanggil oleh GitHub webhook setiap kali ada push ke main

set -e

APP_DIR="/www/wwwroot/django/apps/simapon"
VENV="/www/wwwroot/django/envs/simapon"
LOG="/www/wwwlogs/simapon_deploy.log"

echo "=== Deploy SIMAPON: $(date) ===" >> "$LOG"

cd "$APP_DIR"

# Discard modified pyc bytecode that could block git pull
git checkout -- '**/*.pyc' 2>/dev/null || true

# Pull latest code
git pull origin main >> "$LOG" 2>&1

# Install/update dependencies
"$VENV/bin/python" -m pip install -r requirements.txt >> "$LOG" 2>&1

# Run migrations
DJANGO_SETTINGS_MODULE=SIMAPON.settings_prod "$VENV/bin/python" manage.py migrate --noinput >> "$LOG" 2>&1

# Collect static files
DJANGO_SETTINGS_MODULE=SIMAPON.settings_prod "$VENV/bin/python" manage.py collectstatic --noinput >> "$LOG" 2>&1

# Ensure correct ownership for www user so sqlite and media remain writable
chown -R www:www "$APP_DIR" >> "$LOG" 2>&1

# Restart service
systemctl restart simapon >> "$LOG" 2>&1

echo "=== Deploy selesai: $(date) ===" >> "$LOG"
