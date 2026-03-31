# 🚀 Data Pipeline Failure Prediction System

An end-to-end Machine Learning system that predicts potential failures in data pipelines, provides root cause analysis, and supports both real-time and batch predictions through an interactive dashboard.

---

## 📌 Overview

This project simulates a real-world pipeline monitoring system where:

* Pipeline logs are analyzed
* Failures are predicted in advance
* Root causes are identified
* Results are visualized via a dashboard

---

## 🎯 Features

### 🔹 Real-Time Prediction

* Fetch latest pipeline data from database
* Predict failure instantly

### 🔹 Batch Prediction (CSV Upload)

* Upload pipeline logs
* Get predictions for multiple records
* View results in table format

### 🔹 Manual Prediction

* Enter pipeline parameters manually
* Useful for testing and demos

### 🔹 Root Cause Analysis

* Uses feature importance from ML model
* Explains why failure might occur

### 🔹 Interactive Dashboard

* Clean UI with multiple sections
* Doughnut chart visualization
* Table for bulk predictions

---

## 🧠 Tech Stack

* **Frontend:** HTML, CSS, JavaScript, Chart.js
* **Backend:** Flask (Python)
* **Machine Learning:** Random Forest (Scikit-learn)
* **Database:** PostgreSQL
* **Data Processing:** Pandas, NumPy

---

## 📂 Project Structure

```
pipeline-failure-prediction/
│
├── backend/
│   ├── app.py
│   ├── model.py
│   ├── preprocess.py
│   ├── db.py
│   └── saved_model/
│
├── frontend/
│   └── index.html
│
├── data/
│   └── pipeline_logs.csv
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/shruti1804/Data-Pipeline-Failure-Prediction-System.git
cd Data-Pipeline-Failure-Prediction-System
```

---

### 2️⃣ Setup Virtual Environment

```
python -m venv venv
.\venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Setup Database

* Create PostgreSQL database: `pipeline_db`
* Create table: `pipeline_logs`
* Insert sample data

---

### 5️⃣ Train Model

```
python backend/model.py
```

---

### 6️⃣ Run Backend

```
python backend/app.py
```

---

### 7️⃣ Run Frontend

* Open `frontend/index.html`
* OR use Live Server in VS Code

---

## 🔗 API Endpoints

| Endpoint          | Method | Description                  |
| ----------------- | ------ | ---------------------------- |
| `/predict`        | POST   | Predict failure from input   |
| `/auto_predict`   | GET    | Predict using latest DB data |
| `/upload_predict` | POST   | Bulk prediction from CSV     |
| `/data`           | GET    | Fetch sample data            |
| `/dashboard`      | GET    | Aggregated metrics           |

---

## 📊 Example Output

```json
{
  "prediction": 1,
  "failure_probability": 0.87,
  "top_cause": "cpu_usage",
  "reason": "Failure likely due to high cpu usage"
}
```

---

## 🎯 Key Highlights

* End-to-end ML pipeline
* Real-time + batch prediction system
* Explainable AI (feature importance)
* Full-stack integration
* Interactive dashboard UI

---

## 🚀 Future Improvements

* Deploy project (Render + Vercel)
* Add authentication
* Real-time monitoring dashboard
* Advanced analytics

---

## 👩‍💻 Author

Shruti
B.Tech Data Science Student

---

## ⭐ If you like this project, consider giving it a star!
