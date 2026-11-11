#!/usr/bin/env python3
"""
GitHub Webhook Server untuk SIMAPON
Menjalankan deploy.sh setiap kali ada push ke branch main
"""
import hashlib
import hmac
import json
import logging
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

# ── Konfigurasi ──────────────────────────────────────────────
PORT = 9020
WEBHOOK_SECRET = b"simapon-secret-2026"  # Ganti di GitHub juga!
DEPLOY_SCRIPT = "/www/wwwroot/django/apps/simapon/deploy.sh"
LOG_FILE = "/www/wwwlogs/simapon_webhook.log"
# ─────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)


class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info(format % args)

    def do_POST(self):
        if self.path != "/webhook":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        # Verifikasi signature GitHub
        sig_header = self.headers.get("X-Hub-Signature-256", "")
        expected = "sha256=" + hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()  # type: ignore
        if not hmac.compare_digest(sig_header, expected):
            logging.warning("Webhook signature tidak valid!")
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            return

        try:
            payload = json.loads(body)
        except Exception:
            self.send_response(400)
            self.end_headers()
            return

        ref = payload.get("ref", "")
        if ref != "refs/heads/main":
            logging.info(f"Push ke branch {ref}, skip deploy.")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Skipped (not main)")
            return

        logging.info("Push ke main terdeteksi, menjalankan deploy...")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Deploy dimulai")

        # Jalankan deploy script (non-blocking)
        subprocess.Popen(["bash", DEPLOY_SCRIPT])

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SIMAPON Webhook OK")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    logging.info(f"Webhook server berjalan di port {PORT}")
    server.serve_forever()
