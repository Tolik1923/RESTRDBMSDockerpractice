import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    db_params = {
        'dbname': 'camp',
        'user': 'myuser',
        'password': 'qwezxc',
        'host': 'localhost'
    }

    connection = psycopg2.connect(**db_params)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    try:
        cursor.execute("CREATE DATABASE camp;")
    except psycopg2.errors.DuplicateDatabase:
        cursor.execute("DROP DATABASE camp;")
        cursor.execute("CREATE DATABASE camp;")

    cursor.close()
    connection.close()

    db_params['dbname'] = 'camp'
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            created_date TIMESTAMP DEFAULT current_timestamp,
            updated_date TIMESTAMP DEFAULT current_timestamp,
            title VARCHAR,
            total NUMERIC(10, 2) DEFAULT 0.00
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            order_id INT,
            name VARCHAR,
            price NUMERIC(10, 2),
            quantity INT
        );
    """)

    cursor.close()
    connection.close()

