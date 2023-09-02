import psycopg2

DATABASE_URL = "postgresql://myuser:qwezxc@localhost/camp"

def create_connection():
    return psycopg2.connect(DATABASE_URL)