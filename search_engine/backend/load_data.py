import pandas as pd
import mysql.connector

# Load CSV
df = pd.read_csv("data/products.csv")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="jobuser",
    password="1234",
    database="searchdb"
)

cursor = conn.cursor()

# Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO products (id, name, description, brand, price, rating, category)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row["id"]),
        row["name"],
        row["description"],
        row["brand"],
        int(row["price"]),
        float(row["rating"]),
        row["category"]
    ))

conn.commit()

cursor.close()
conn.close()

print("Data inserted successfully!")