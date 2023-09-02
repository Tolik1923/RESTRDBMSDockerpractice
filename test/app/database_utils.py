from database import create_connection 
import psycopg2

def update_order_update_time(order_id: int):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE orders SET update_time = NOW() WHERE id = %s",
            (order_id,)
        )


    except psycopg2.Error as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

