import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="pipeline_db",
        user="postgres",
        password="system",
        host="localhost",
        port="5432"
    )
    return conn
