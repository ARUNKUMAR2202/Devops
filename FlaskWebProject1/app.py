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

    return f"""
    <h1>Docker Compose Lab</h1>

    <h3>Student Information</h3>
    <p><b>Name:</b> Arun Kumar</p>
    <p><b>Class:</b> DevOps</p>

    <h3>System Information</h3>
    <p><b>Instance:</b> {INSTANCE}</p>
    <p><b>Version:</b> {VERSION}</p>
    <p><b>Current Time:</b> {current_time}</p>
    <p><b>Status:</b> Running Successfully</p>

    <hr>

    <h3>Available Endpoints</h3>
    <ul>
        <li><a href="/hello/Arun">Hello Endpoint</a></li>
        <li><a href="/add/5/3">Add Numbers</a></li>
        <li><a href="/data">Random Data</a></li>
        <li><a href="/mysql-time">MySQL Time</a></li>
        <li><a href="/version">Version</a></li>
    </ul>
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