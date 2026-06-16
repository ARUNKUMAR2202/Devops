
import mysql.connector
from FlaskWebProject1 import app
from flask import jsonify

@app.route("/version")
def version():
    return jsonify({"version": "1.0"})

@app.route('/db')
def db_test():
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password="root123",
        database="mysql"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return f"MySQL Connected: {result}"

<<<<<<< HEAD

=======
>>>>>>> 2626f148537bf0b16f246999423668391734748f
