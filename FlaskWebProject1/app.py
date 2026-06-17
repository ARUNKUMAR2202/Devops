from flask import Flask, jsonify
import random
import pymysql
import os
from datetime import datetime

app = Flask(__name__)

INSTANCE = os.environ.get("INSTANCE_NAME", "flask-app")
VERSION  = os.environ.get("APP_VERSION", "1.0")

# --- Logic from code1.py ---
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# --- Logic from helpers2.py ---
def getData():
    data = ["apple", "banana", "cherry"]
    return data[random.randint(0, len(data) - 1)]

def getData2():
    data = ["dog", "cat", "mouse"]
    return data[random.randint(0, len(data) - 1)]

def getData3():
    data = ["red", "green", "blue"]
    return data[random.randint(0, len(data) - 1)]

# --- Routes ---

@app.route("/")
def home():
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    accent = "#5EE0A6" if INSTANCE == "flask-app-1" else "#7FB2FF" if INSTANCE == "flask-app-2" else "#F2C879"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{INSTANCE} :: status</title>
<style>
  :root {{
    --bg: #0B0E11;
    --panel: #11151A;
    --line: #1E242B;
    --text: #D8DEE4;
    --muted: #6B7785;
    --accent: {accent};
  }}

  * {{ box-sizing: border-box; }}

  body {{
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: 'IBM Plex Mono', 'SF Mono', 'Consolas', monospace;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 32px;
  }}

  .card {{
    width: 100%;
    max-width: 640px;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 4px;
    overflow: hidden;
  }}

  .titlebar {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    border-bottom: 1px solid var(--line);
    background: #0D1014;
  }}

  .dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
  }}

  .titlebar span {{
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 0.04em;
  }}

  .body {{
    padding: 28px 28px 24px;
  }}

  .eyebrow {{
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 6px;
  }}

  h1 {{
    margin: 0 0 24px;
    font-size: 26px;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
  }}

  h1 .accent {{ color: var(--accent); }}

  .grid {{
    display: grid;
    grid-template-columns: 120px 1fr;
    row-gap: 12px;
    font-size: 14px;
    border-top: 1px solid var(--line);
    padding-top: 18px;
  }}

  .grid dt {{
    color: var(--muted);
  }}

  .grid dd {{
    margin: 0;
    color: var(--text);
  }}

  .status-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: var(--accent);
  }}

  .status-pill::before {{
    content: "";
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
  }}

  .divider {{
    height: 1px;
    background: var(--line);
    margin: 22px 0 18px;
  }}

  nav {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}

  nav a {{
    color: var(--muted);
    text-decoration: none;
    font-size: 13px;
    padding: 6px 10px;
    border: 1px solid var(--line);
    border-radius: 3px;
    transition: border-color 0.15s, color 0.15s;
  }}

  nav a:hover {{
    border-color: var(--accent);
    color: var(--text);
  }}

  .footer {{
    padding: 12px 28px;
    border-top: 1px solid var(--line);
    font-size: 11px;
    color: var(--muted);
    display: flex;
    justify-content: space-between;
  }}
</style>
</head>
<body>
  <div class="card">
    <div class="titlebar">
      <div class="dot"></div>
      <span>{INSTANCE}.local — flask dev server</span>
    </div>
    <div class="body">
      <p class="eyebrow">Docker Compose Lab</p>
      <h1>Arun Kumar <span class="accent">// DevOps</span></h1>

      <dl class="grid">
        <dt>instance</dt>
        <dd>{INSTANCE}</dd>

        <dt>version</dt>
        <dd>{VERSION}</dd>

        <dt>status</dt>
        <dd><span class="status-pill">running</span></dd>

        <dt>checked</dt>
        <dd>{current_time}</dd>
      </dl>

      <div class="divider"></div>

      <nav>
        <a href="/hello/Arun">/hello/Arun</a>
        <a href="/add/5/3">/add/5/3</a>
        <a href="/data">/data</a>
        <a href="/mysql-time">/mysql-time</a>
        <a href="/version">/version</a>
      </nav>
    </div>
    <div class="footer">
      <span>nginx → upstream</span>
      <span>refresh to re-poll</span>
    </div>
  </div>
</body>
</html>
"""

@app.route("/hello/<name>")
def hello(name):
    return jsonify(message=f"Hello, {name}!", data=getData())

@app.route("/add/<int:a>/<int:b>")
def add_route(a, b):
    return jsonify(result=add(a, b))

@app.route("/data")
def data_route():
    return jsonify(
        fruit=getData(),
        animal=getData2(),
        color=getData3()
    )

# --- MySQL Time Endpoint ---
@app.route("/mysql-time")
def mysql_time():
    try:
        conn = pymysql.connect(
            host=os.environ.get("MYSQL_HOST", "mysql"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", "root123"),
            database=os.environ.get("MYSQL_DB", "mysql"),
            connect_timeout=5
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT CURRENT_TIMESTAMP()")
            result = cursor.fetchone()
        conn.close()
        return jsonify(mysql_time=str(result[0]), status="connected")
    except Exception as e:
        return jsonify(error=str(e), status="MySQL not reachable"), 500

# --- Version / Instance identity endpoint (used for load-balancing demo) ---
@app.route("/version")
def version():
    return jsonify(instance=INSTANCE, version=VERSION)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)