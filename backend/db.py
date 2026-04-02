def get_connection():
    try:
        import psycopg2
        return psycopg2.connect(
            dbname="pipeline_db",
            user="postgres",
            password="your_password",
            host="localhost",
            port="5432"
        )
    except:
        return None