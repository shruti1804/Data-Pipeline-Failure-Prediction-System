import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

data = {
    "pipeline_id": np.random.randint(1, 50, rows),
    "execution_time": np.random.normal(200, 50, rows),
    "records_processed": np.random.randint(1000, 20000, rows),
    "error_count": np.random.randint(0, 15, rows),
    "cpu_usage": np.random.uniform(40, 100, rows),
    "memory_usage": np.random.uniform(30, 95, rows),
    "data_delay": np.random.uniform(0, 30, rows),
}

df = pd.DataFrame(data)

# Failure logic (important for ML)
df["status"] = (
    (df["error_count"] > 8) |
    (df["cpu_usage"] > 85) |
    (df["execution_time"] > 300)
).astype(int)

df.to_csv("data/pipeline_logs.csv", index=False)

print("Dataset generated successfully!")