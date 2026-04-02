import joblib
import os
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_connection

app = Flask(__name__)
CORS(app)

model = joblib.load("backend/saved_model/model.pkl")
scaler = joblib.load("backend/saved_model/scaler.pkl")

FEATURE_NAMES = [
    "pipeline_id",
    "execution_time",
    "records_processed",
    "error_count",
    "cpu_usage",
    "memory_usage",
    "data_delay"
]

# ─────────────────────────────────────────────
#  SHAP-style per-prediction feature importance
#  Uses a lightweight manual approach:
#  For each feature, we measure how much the
#  predicted probability changes when that
#  feature is set to its "baseline" (mean of
#  training-like neutral values). The delta
#  tells us how much that feature "pushed" the
#  prediction vs a neutral baseline.
# ─────────────────────────────────────────────

# Neutral baseline — midpoint of typical ranges
# Adjust these to match your actual training data distribution
FEATURE_BASELINE = [
    1,       # pipeline_id  (arbitrary, low weight expected)
    60.0,    # execution_time (seconds) — moderate
    10000,   # records_processed — moderate
    2,       # error_count — low-normal
    50.0,    # cpu_usage (%) — moderate
    50.0,    # memory_usage (%) — moderate
    1.0      # data_delay (seconds) — low-normal
]

def compute_per_prediction_importance(features_raw: list) -> dict:
    """
    Computes per-prediction feature contributions using
    the "leave-one-at-baseline" ablation method.

    For each feature i:
      contribution[i] = P(fail | actual input)
                      - P(fail | input with feature_i replaced by baseline)

    Positive value  → feature is PUSHING the prediction TOWARD failure
    Negative value  → feature is PULLING the prediction AWAY from failure

    Returns a dict with feature names as keys and contribution scores as values.
    """
    baseline = np.array(FEATURE_BASELINE, dtype=float)
    actual   = np.array(features_raw, dtype=float)

    # Full prediction probability with actual input
    actual_scaled = scaler.transform(actual.reshape(1, -1))
    p_full = model.predict_proba(actual_scaled)[0][1]

    contributions = {}

    for i, name in enumerate(FEATURE_NAMES):
        # Replace feature i with baseline value, keep rest actual
        ablated = actual.copy()
        ablated[i] = baseline[i]

        ablated_scaled = scaler.transform(ablated.reshape(1, -1))
        p_ablated = model.predict_proba(ablated_scaled)[0][1]

        # How much does this feature contribute to the risk?
        contributions[name] = round(float(p_full - p_ablated), 6)

    return contributions


def build_explanation(contributions: dict, prediction: int) -> str:
    """
    Build a human-readable explanation from contributions.
    """
    # Sort by absolute magnitude
    sorted_contribs = sorted(contributions.items(), key=lambda x: abs(x[1]), reverse=True)
    top_driver = sorted_contribs[0]

    direction = "increasing" if top_driver[1] > 0 else "reducing"
    action = "failure" if prediction == 1 else "stability"

    return (
        f"Primary driver: '{top_driver[0].replace('_', ' ')}' is {direction} "
        f"risk by {abs(top_driver[1]*100):.1f}pp, contributing most to predicted {action}."
    )


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def home():
    return {"message": "PipelineGuard API running"}


# ── DATA RETRIEVAL ────────────────────────────
@app.route("/data")
def get_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pipeline_logs LIMIT 10;")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in rows])


# ── PREDICTION + PER-PREDICTION SHAP ─────────
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features_raw = [
        data["pipeline_id"],
        data["execution_time"],
        data["records_processed"],
        data["error_count"],
        data["cpu_usage"],
        data["memory_usage"],
        data["data_delay"]
    ]

    features = np.array(features_raw).reshape(1, -1)
    features_scaled = scaler.transform(features)

    prediction   = int(model.predict(features_scaled)[0])
    probability  = float(model.predict_proba(features_scaled)[0][1])

    # ── Per-prediction contributions (SHAP-style) ──
    contributions = compute_per_prediction_importance(features_raw)

    # Sort contributions for easy frontend rendering
    sorted_contributions = sorted(
        [{"feature": k, "contribution": v} for k, v in contributions.items()],
        key=lambda x: abs(x["contribution"]),
        reverse=True
    )

    # Top positive (risk drivers) and top negative (stabilizers)
    risk_drivers  = [c for c in sorted_contributions if c["contribution"] > 0]
    stabilizers   = [c for c in sorted_contributions if c["contribution"] <= 0]

    top_cause = sorted_contributions[0]["feature"] if sorted_contributions else "unknown"
    reason    = build_explanation(contributions, prediction)

    return jsonify({
        "prediction":          prediction,
        "failure_probability": probability,
        "top_cause":           top_cause,
        "reason":              reason,

        # Full per-feature contributions sorted by impact magnitude
        # Positive = pushes toward failure, Negative = stabilizing
        "feature_contributions": sorted_contributions,

        # Convenience splits
        "risk_drivers":  risk_drivers[:3],
        "stabilizers":   stabilizers[:3],

        # Global model importances (unchanged from before)
        "global_importances": dict(zip(FEATURE_NAMES, model.feature_importances_.tolist()))
    })


# ── DASHBOARD ────────────────────────────────
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

    return jsonify({
        "avg_execution_time": result[0],
        "avg_error_count":    result[1],
        "avg_cpu_usage":      result[2]
    })


# ── AUTO PREDICT ──────────────────────────────
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

    features_raw  = list(row)
    features      = np.array(features_raw).reshape(1, -1)
    features_scaled = scaler.transform(features)

    prediction  = int(model.predict(features_scaled)[0])
    probability = float(model.predict_proba(features_scaled)[0][1])

    contributions = compute_per_prediction_importance(features_raw)
    sorted_contributions = sorted(
        [{"feature": k, "contribution": v} for k, v in contributions.items()],
        key=lambda x: abs(x["contribution"]),
        reverse=True
    )

    reason = build_explanation(contributions, prediction)

    return jsonify({
        "data":                  features_raw,
        "prediction":            prediction,
        "failure_probability":   probability,
        "reason":                reason,
        "feature_contributions": sorted_contributions,
        "risk_drivers":          [c for c in sorted_contributions if c["contribution"] > 0][:3],
        "stabilizers":           [c for c in sorted_contributions if c["contribution"] <= 0][:3],
    })


# ── BULK / UPLOAD PREDICT ─────────────────────
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
        return jsonify({"error": "No data found"})

    features_raw    = list(row)
    features        = np.array(features_raw).reshape(1, -1)
    features_scaled = scaler.transform(features)

    prediction  = int(model.predict(features_scaled)[0])
    probability = float(model.predict_proba(features_scaled)[0][1])

    contributions = compute_per_prediction_importance(features_raw)
    sorted_contributions = sorted(
        [{"feature": k, "contribution": v} for k, v in contributions.items()],
        key=lambda x: abs(x["contribution"]),
        reverse=True
    )

    return jsonify({
        "prediction":            prediction,
        "failure_probability":   probability,
        "reason":                build_explanation(contributions, prediction),
        "feature_contributions": sorted_contributions,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))