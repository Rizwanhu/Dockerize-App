"""Small sample web app used to demonstrate containerization."""
import os
import platform
import socket
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "TechAbout Docker Demo")
APP_ENV = os.getenv("APP_ENV", "development")
START_TIME = datetime.now(timezone.utc)

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ name }}</title>
<style>
 body{font-family:system-ui,Segoe UI,Arial,sans-serif;background:#0f172a;color:#e2e8f0;margin:0;display:grid;place-items:center;min-height:100vh}
 .card{background:#1e293b;border-radius:14px;padding:32px 40px;max-width:520px;width:90%;box-shadow:0 10px 30px #0006}
 h1{margin:0 0 6px;font-size:26px} .ok{color:#4ade80;font-weight:600}
 table{width:100%;border-collapse:collapse;margin-top:18px} td{padding:8px 0;border-bottom:1px solid #334155}
 td:first-child{color:#94a3b8;width:40%} code{color:#7dd3fc}
</style></head><body><div class="card">
<h1>{{ name }}</h1>
<div class="ok">&#9679; App is running</div>
<table>
 <tr><td>Container hostname</td><td><code>{{ host }}</code></td></tr>
 <tr><td>Environment</td><td><code>{{ env }}</code></td></tr>
 <tr><td>Python</td><td><code>{{ py }}</code></td></tr>
 <tr><td>Started (UTC)</td><td><code>{{ started }}</code></td></tr>
 <tr><td>Uptime</td><td><code>{{ uptime }}</code></td></tr>
</table>
<p style="color:#94a3b8;font-size:13px">Endpoints: <code>/</code> &middot; <code>/health</code> &middot; <code>/api/info</code></p>
</div></body></html>"""


def info():
    now = datetime.now(timezone.utc)
    return {
        "app": APP_NAME,
        "environment": APP_ENV,
        "hostname": socket.gethostname(),
        "python": platform.python_version(),
        "started_utc": START_TIME.strftime("%Y-%m-%d %H:%M:%S"),
        "uptime_seconds": int((now - START_TIME).total_seconds()),
    }


@app.route("/")
def index():
    d = info()
    return render_template_string(
        PAGE, name=d["app"], host=d["hostname"], env=d["environment"],
        py=d["python"], started=d["started_utc"], uptime=f'{d["uptime_seconds"]}s',
    )


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/api/info")
def api_info():
    return jsonify(info())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
