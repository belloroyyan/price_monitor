# database.py
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "tracker.db")

def init_db():
    """Initializes the database and creates the history table if it doesn't exist."""
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                url TEXT NOT NULL,
                price REAL NOT NULL,
                is_in_stock INTEGER NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

def log_price_data(name, url, price, is_in_stock):
    """Inserts a new historical data point into the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO price_history (product_name, url, price, is_in_stock, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, url, price, int(is_in_stock), datetime.now().isoformat()))
        conn.commit()
