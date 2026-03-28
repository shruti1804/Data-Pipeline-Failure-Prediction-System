import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from preprocess import preprocess_data

# Load data
df = pd.read_csv("data/pipeline_logs.csv")

# Preprocess
X, y, scaler = preprocess_data(df)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy}")

# Save model + scaler
joblib.dump(model, "backend/saved_model/model.pkl")
joblib.dump(scaler, "backend/saved_model/scaler.pkl")

print("Model and scaler saved!")

# ---------------- ROOT CAUSE ANALYSIS ----------------

# Get feature importance
importance = model.feature_importances_

# Feature names
feature_names = [
    "pipeline_id",
    "execution_time",
    "records_processed",
    "error_count",
    "cpu_usage",
    "memory_usage",
    "data_delay"
]

# Create dataframe for better visualization
importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importance
}).sort_values(by="importance", ascending=False)

print("\nFeature Importance:")
print(importance_df)