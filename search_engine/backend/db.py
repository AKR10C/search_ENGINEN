import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "jobuser"),
        password=os.getenv("DB_PASSWORD", "1234"),
        database=os.getenv("DB_NAME", "searchdb")
    )

def get_products_by_ids(ids, max_price=None, min_rating=None, sort_option=None):
    if not ids:
        return []

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = f"""
            SELECT * FROM products
            WHERE id IN ({','.join(['%s'] * len(ids))})
        """

        params = ids.copy()

        if max_price:
            query += " AND price <= %s"
            params.append(max_price)
        if min_rating:
            query += " AND rating >= %s"
            params.append(min_rating)
        if sort_option:
            # Validate column name to prevent SQL injection
            allowed_columns = ["price", "rating", "name", "id"]
            column, order = sort_option
            if column not in allowed_columns:
                raise ValueError(f"Invalid sort column: {column}")
            if order.upper() not in ["ASC", "DESC"]:
                raise ValueError(f"Invalid sort order: {order}")
            query += f" ORDER BY {column} {order.upper()}"

        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()