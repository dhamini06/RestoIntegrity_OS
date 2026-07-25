import sqlite3
import os
import json
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resto_integrity.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL, -- admin, staff, kitchen, customer
        full_name TEXT NOT NULL
    )
    """)
    
    # 2. Menu Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT NOT NULL, -- Starter, Main, Dessert, Beverage
        is_available INTEGER DEFAULT 1, -- 0 for false, 1 for true
        stock_level INTEGER DEFAULT 100
    )
    """)
    
    # 3. Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_number TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending', -- pending, preparing, completed, voided
        subtotal REAL NOT NULL,
        discount REAL DEFAULT 0,
        total REAL NOT NULL,
        discount_applied_by TEXT, -- username of staff/admin
        created_at TEXT NOT NULL
    )
    """)
    
    # 4. Order Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        menu_item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
    )
    """)
    
    # 5. Inventory Ingredients/Items Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT UNIQUE NOT NULL,
        current_quantity REAL NOT NULL,
        min_threshold REAL NOT NULL,
        unit TEXT NOT NULL, -- kg, liters, units, etc.
        last_updated TEXT NOT NULL
    )
    """)
    
    # 6. Security Alerts (SOC-style operational integrity log)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS security_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT NOT NULL, -- void_anomaly, discount_anomaly, shrinkage_anomaly
        severity TEXT NOT NULL, -- low, medium, high, critical
        details TEXT NOT NULL, -- JSON string representation
        triggered_by TEXT, -- username of user responsible if applicable
        ai_analysis TEXT, -- Gemini-powered investigation report (JSON/Text)
        status TEXT NOT NULL DEFAULT 'active', -- active, investigated, resolved
        created_at TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", DB_FILE)
