from database import create_connection 
#from database_utils import update_order_update_time
import psycopg2

def get_all_orders():
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM orders"
    cursor.execute(query)

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return orders

def get_order_by_id(order_id: int):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM orders WHERE id = %s"
    cursor.execute(query, (order_id,))

    order = cursor.fetchone()

    cursor.close()
    conn.close()

    return order

def create_order(order_data):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO orders (title, total, created_date, updated_date) VALUES (%s, %s, DEFAULT, DEFAULT) RETURNING id",
            (order_data['title'], order_data['total'])
        )

        order_id = cursor.fetchone()[0]

        for item in order_data['items']:
            cursor.execute(
                "INSERT INTO items (order_id, name, price, quantity) VALUES (%s, %s, %s, %s)",
                (order_id, item['name'], item['price'], item['quantity'])
            )

        conn.commit()
        return order_id

    except psycopg2.Error as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

def update_order_by_id(order_id: int, order_data: dict):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE orders SET title = %s, total = %s, updated_date = NOW() WHERE id = %s",
            (order_data['title'], order_data['total'], order_id)
        )
        
        updated_order_id = order_id
        
        conn.commit()
        return updated_order_id

    except psycopg2.Error as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

def delete_order(order_id: int):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM items WHERE order_id = %s", (order_id,))
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    except psycopg2.Error as e:
        conn.rollback()
        raise e
        
    finally:
        cursor.close()
        conn.close()

def get_stats():
    conn = create_connection()
    cursor = conn.cursor()

    try:
   
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total) FROM orders")
        total_order_price = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(total) FROM orders")
        avg_order_price = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(quantity) FROM items")
        total_items = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(quantity) FROM items")
        avg_items = cursor.fetchone()[0]

        cursor.execute(
            "SELECT name FROM items GROUP BY name ORDER BY SUM(quantity) DESC LIMIT 1"
        )
        most_ordered_item = cursor.fetchone()[0]

        stats = {
            "total_orders": total_orders,
            "total_order_price": total_order_price,
            "avg_order_price": avg_order_price,
            "total_items": total_items,
            "avg_items": avg_items,
            "most_ordered_item": most_ordered_item,
        }

        return stats
    
    finally:
        cursor.close()
        conn.close()

def get_order_items(order_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM items WHERE order_id = %s", (order_id,))
        items = cursor.fetchall()
        return items

    finally:
        cursor.close()
        conn.close()

async def get_order_item(order_id: int, item_id: int):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM items WHERE order_id = %s AND id = %s"
    cursor.execute(query, (order_id, item_id))

    item = cursor.fetchone()

    cursor.close()
    conn.close()

    return item

async def add_item_to_order(order_id: int, item_data: dict):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO items (order_id, name, price, quantity) VALUES (%s, %s, %s, %s) RETURNING id",
            (order_id, item_data['name'], item_data['price'], item_data['quantity'])
        )
        item_id = cursor.fetchone()[0]
        #update_order_update_time(order_id)
        conn.commit()
        return item_id

    except psycopg2.Error as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

async def update_order_item(order_id: int, item_id: int, item_data: dict):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE items SET name = %s, price = %s, quantity = %s WHERE id = %s AND order_id = %s",
            (item_data['name'], item_data['price'], item_data['quantity'], item_id, order_id)
        )
        #update_order_update_time(order_id)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

async def delete_order_item(order_id: int, item_id: int):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM items WHERE id = %s AND order_id = %s",
            (item_id, order_id)
        )
        #update_order_update_time(order_id)
        conn.commit()

    except psycopg2.Error as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()
