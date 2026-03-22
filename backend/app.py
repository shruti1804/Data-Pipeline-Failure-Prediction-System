from flask import Flask, jsonify
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"message": "API running"}

@app.route("/data")
def get_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pipeline_logs LIMIT 10;")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)