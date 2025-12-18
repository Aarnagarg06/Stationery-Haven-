# db.py
import sqlite3

DB_NAME = "stock.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            quantity INTEGER
        )
    """)
    conn.commit()
    conn.close()

def insert_product(name, price, quantity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
        (name, price, quantity)
    )
    conn.commit()
    conn.close()

def get_all_products():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, price, quantity FROM products")
    data = cur.fetchall()
    conn.close()
    return data

