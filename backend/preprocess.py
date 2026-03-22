import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(df):
    # Handle missing values (just in case)
    df = df.fillna(df.mean())

    # Separate features & target
    X = df.drop("status", axis=1)
    y = df["status"]

    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, scaler