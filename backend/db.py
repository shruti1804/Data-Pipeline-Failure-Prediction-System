import psycopg2
import os

def get_connection():
    conn = psycopg2.connect(
        dbname   = os.environ.get("DB_NAME",     "pipeline_db"),
        user     = os.environ.get("DB_USER",     "postgres"),
        password = os.environ.get("DB_PASSWORD", "system"),
        host     = os.environ.get("DB_HOST",     "localhost"),
        port     = os.environ.get("DB_PORT",     "5432")
    )
    return conn
