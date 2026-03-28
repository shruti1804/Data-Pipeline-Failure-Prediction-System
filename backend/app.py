import joblib
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)

model = joblib.load("backend/saved_model/model.pkl")
scaler = joblib.load("backend/saved_model/scaler.pkl")

@app.route("/")
def home():
    return {"message": "API running"}

#----------------- DATA RETRIEVAL ----------------
@app.route("/data")
def get_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pipeline_logs LIMIT 10;")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    return jsonify(result)

#----------------- PREDICTION & ROOT CAUSE ----------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = [
        data["pipeline_id"],
        data["execution_time"],
        data["records_processed"],
        data["error_count"],
        data["cpu_usage"],
        data["memory_usage"],
        data["data_delay"]
    ]

    features = np.array(features).reshape(1, -1)

    # Scale input
    features_scaled = scaler.transform(features)

    # Prediction
    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]

    # ---------------- ROOT CAUSE ----------------
    importances = model.feature_importances_

    feature_names = [
        "pipeline_id",
        "execution_time",
        "records_processed",
        "error_count",
        "cpu_usage",
        "memory_usage",
        "data_delay"
    ]

    # Pair & sort
    feature_impact = list(zip(feature_names, importances))
    feature_impact.sort(key=lambda x: x[1], reverse=True)

    top_feature = feature_impact[0][0]

    reason = f"Failure likely due to high {top_feature.replace('_', ' ')}"

    # Return response
    return {
        "prediction": int(prediction),
        "failure_probability": float(probability),
        "top_cause": top_feature,
        "reason": reason
    }

#----------------- DASHBOARD ----------------    
@app.route("/dashboard", methods=["GET"])
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(execution_time), AVG(error_count), AVG(cpu_usage)
        FROM pipeline_logs;
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return {
        "avg_execution_time": result[0],
        "avg_error_count": result[1],
        "avg_cpu_usage": result[2]
    }



#----------------- AUTO PREDICT ----------------
@app.route("/auto_predict", methods=["GET"])
def auto_predict():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pipeline_id, execution_time, records_processed,
               error_count, cpu_usage, memory_usage, data_delay
        FROM pipeline_logs
        ORDER BY id DESC
        LIMIT 1;
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    features = np.array(row).reshape(1, -1)
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]

    return {
        "data": list(row),
        "prediction": int(prediction),
        "failure_probability": float(probability)
    }

#----------------- BULK PREDICTION ----------------
@app.route("/upload_predict", methods=["POST"])
def upload_predict():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pipeline_id, execution_time, records_processed,
               error_count, cpu_usage, memory_usage, data_delay
        FROM pipeline_logs
        ORDER BY id DESC
        LIMIT 1;
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row is None:
        return {"error": "No data found"}

    import numpy as np

    features = np.array(row).reshape(1, -1)
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]
    probability = model.predict_proba(features_scaled)[0][1]

    return {
        "prediction": int(prediction),
        "failure_probability": float(probability),
        "reason": "Auto fetched latest pipeline data"
    }
    
if __name__ == "__main__":
    app.run(debug=True)