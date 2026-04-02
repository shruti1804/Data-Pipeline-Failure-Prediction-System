# 🚀 Data Pipeline Failure Prediction System

An end-to-end **Machine Learning + Full-Stack application** that predicts potential failures in data pipelines, provides root cause analysis, and visualizes insights through an interactive dashboard.

---

## 🌐 Live Demo

- 🔗 Frontend: pipelineguard.netlify.app
- 🔗 Backend API: https://pipelineguard-api.onrender.com

---

## 📌 Overview

Modern data pipelines are critical for analytics systems, but failures can disrupt operations.

This project shifts monitoring from **reactive → proactive** by:
- Predicting failures before they occur
- Identifying root causes
- Providing actionable insights via dashboard

---

## 🎯 Features

### ⚡ Real-Time Prediction
- Fetch latest pipeline data from database
- Predict failure instantly using trained ML model

### 📂 Batch Prediction (CSV Upload)
- Upload pipeline logs
- Predict multiple records at once
- View results in structured table format

### ✍️ Manual Prediction
- Input pipeline parameters manually
- Ideal for testing and demonstrations

### 🧠 Root Cause Analysis
- Uses feature importance from Random Forest
- Explains **why a failure might occur**

### 📊 Interactive Dashboard
- Clean UI with multiple sections
- Doughnut chart visualization
- Data tables for insights

---

## 🧠 Tech Stack

| Layer | Technology |
|------|-----------|
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Backend | Flask (Python) |
| Machine Learning | Random Forest (Scikit-learn) |
| Database | PostgreSQL (Render) |
| Data Processing | Pandas, NumPy |
| Deployment | Render (Backend), Netlify (Frontend) |

---

## 🏗️ System Architecture

```
Frontend (Netlify)
↓
Flask API (Render)
↓
PostgreSQL Database (Render)
↓
Machine Learning Model
```

## 📂 Project Structure

```
pipeline-failure-prediction/
│
├── backend/
│   ├── app.py
│   ├── model.py
│   ├── preprocess.py
│   ├── db.py
|   |── requiremnts.txt
|   |── Procfile
│   └── saved_model/
|        ├── model.pkl
|        └── scaler.pkl
|   
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

## 🔗 API Endpoints

| Endpoint | Method | Description |
|--------|--------|------------|
| `/` | GET | API health check |
| `/data` | GET | Fetch pipeline data |
| `/predict` | POST | Predict failure from input |
| `/auto_predict` | GET | Predict using latest DB data |
| `/upload_predict` | POST | Bulk prediction from CSV |
| `/dashboard` | GET | Aggregated metrics |

---

## 📊 Example Output

```json
{
  "prediction": 1,
  "failure_probability": 0.87,
  "top_cause": "cpu_usage",
  "reason": "Failure likely due to high cpu usage"
}
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

* ✅ End-to-end ML system
* ✅ Real-time + batch prediction
* ✅ Explainable AI (feature importance)
* ✅ Cloud deployment (Render + Netlify)
* ✅ Full-stack integration

---

## 🚀 Future Improvements

* Authentication system
* Real-time streaming (Kafka)
* Advanced ML models (XGBoost)
* Alert system (Email/SMS)

---

## 👩‍💻 Author

Shruti Wadnerkar

---

## ⭐ If you like this project, consider giving it a star!
