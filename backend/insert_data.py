import pandas as pd
from db import get_connection

df = pd.read_csv("data/pipeline_logs.csv")

conn = get_connection()
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO pipeline_logs (
            pipeline_id, execution_time, records_processed,
            error_count, cpu_usage, memory_usage, data_delay, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row["pipeline_id"]),
        float(row["execution_time"]),
        int(row["records_processed"]),
        int(row["error_count"]),
        float(row["cpu_usage"]),
        float(row["memory_usage"]),
        float(row["data_delay"]),
        int(row["status"])
    ))

conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully!")