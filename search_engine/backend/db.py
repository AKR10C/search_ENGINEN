import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="jobuser",
        password="1234",
        database="searchdb"
    )

def get_products_by_ids(ids, max_price=None, min_rating=None, sort_option=None):
    if not ids:
        return []

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"""
        SELECT * FROM products
        WHERE id IN ({','.join(['%s'] * len(ids))})
    """

    params = ids.copy()

    # 🔥 add this
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)
    #filter based on rating 
    if min_rating:
        query += " AND rating >= %s"
        params.append(min_rating)
    #sort 
    if sort_option:
        column, order = sort_option
        query += f" ORDER BY {column} {order.upper()}"

    cursor.execute(query, params)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results