import sqlite3
import os
import json
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resto_integrity.db")

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'staff',
        avatar_url TEXT,
        google_id TEXT UNIQUE,
        email_verified INTEGER DEFAULT 0,
        is_active INTEGER DEFAULT 1,
        last_login TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        session_token TEXT UNIQUE NOT NULL,
        ip_address TEXT,
        device_info TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TEXT NOT NULL,
        last_activity TEXT NOT NULL,
        expires_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        otp_hash TEXT NOT NULL,
        purpose TEXT NOT NULL DEFAULT 'login',
        attempts_remaining INTEGER NOT NULL DEFAULT 5,
        expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        verified_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        email TEXT NOT NULL,
        event_type TEXT NOT NULL,
        status TEXT NOT NULL,
        ip_address TEXT,
        device_info TEXT,
        details TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_login_history_email ON login_history(email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_login_history_user ON login_history(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_otp_requests_email ON otp_requests(email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_user ON user_sessions(user_id)")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        is_available INTEGER DEFAULT 1,
        stock_level INTEGER DEFAULT 100
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_number TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        subtotal REAL NOT NULL,
        discount REAL DEFAULT 0,
        total REAL NOT NULL,
        tax REAL DEFAULT 0,
        tip REAL DEFAULT 0,
        payment_method TEXT DEFAULT 'Cash',
        discount_applied_by TEXT,
        served_by TEXT,
        created_at TEXT NOT NULL,
        prepping_at TEXT,
        completed_at TEXT
    )
    """)

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT UNIQUE NOT NULL,
        current_quantity REAL NOT NULL,
        min_threshold REAL NOT NULL,
        unit TEXT NOT NULL,
        last_updated TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS security_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_type TEXT NOT NULL,
        severity TEXT NOT NULL,
        details TEXT NOT NULL,
        triggered_by TEXT,
        ai_analysis TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingredient_name TEXT NOT NULL,
        current_qty REAL NOT NULL,
        threshold REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        created_at TEXT NOT NULL,
        resolved_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurant_tables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_number TEXT UNIQUE NOT NULL,
        capacity INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'available',
        location TEXT DEFAULT 'Main Hall'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        customer_email TEXT,
        phone TEXT,
        party_size INTEGER NOT NULL,
        table_id INTEGER,
        reservation_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'confirmed',
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (table_id) REFERENCES restaurant_tables(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT NOT NULL DEFAULT 'info',
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        phone TEXT,
        party_size INTEGER NOT NULL,
        table_id INTEGER,
        status TEXT NOT NULL DEFAULT 'waiting',
        position INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        seated_at TEXT,
        notes TEXT,
        FOREIGN KEY (table_id) REFERENCES restaurant_tables(id)
    )
    """)

    conn.commit()
    conn.close()

def migrate_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA table_info(orders)")
        cols = [row[1] for row in cursor.fetchall()]
        migrations = {
            'prepping_at': "ALTER TABLE orders ADD COLUMN prepping_at TEXT",
            'completed_at': "ALTER TABLE orders ADD COLUMN completed_at TEXT",
            'tax': "ALTER TABLE orders ADD COLUMN tax REAL DEFAULT 0",
            'tip': "ALTER TABLE orders ADD COLUMN tip REAL DEFAULT 0",
            'payment_method': "ALTER TABLE orders ADD COLUMN payment_method TEXT DEFAULT 'Cash'",
            'served_by': "ALTER TABLE orders ADD COLUMN served_by TEXT",
        }
        for col, sql in migrations.items():
            if col not in cols:
                cursor.execute(sql)
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(restaurant_tables)")
        if not cursor.fetchall():
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS restaurant_tables (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_number TEXT UNIQUE NOT NULL,
                    capacity INTEGER NOT NULL,
                    status TEXT NOT NULL DEFAULT 'available',
                    location TEXT DEFAULT 'Main Hall'
                )
            """)
            for i in range(1, 9):
                cursor.execute(
                    "INSERT OR IGNORE INTO restaurant_tables (table_number, capacity, location) VALUES (?, ?, ?)",
                    (f"Table {i}", 4 if i % 2 == 0 else 2, "Main Hall")
                )
        cursor.execute("PRAGMA table_info(reservations)")
        if not cursor.fetchall():
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    customer_email TEXT,
                    phone TEXT,
                    party_size INTEGER NOT NULL,
                    table_id INTEGER,
                    reservation_time TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'confirmed',
                    notes TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id)
                )
            """)
        cursor.execute("PRAGMA table_info(notifications)")
        if not cursor.fetchall():
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    role TEXT,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    type TEXT NOT NULL DEFAULT 'info',
                    is_read INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
        cursor.execute("PRAGMA table_info(queue)")
        if not cursor.fetchall():
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    phone TEXT,
                    party_size INTEGER NOT NULL,
                    table_id INTEGER,
                    status TEXT NOT NULL DEFAULT 'waiting',
                    position INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    seated_at TEXT,
                    notes TEXT,
                    FOREIGN KEY (table_id) REFERENCES restaurant_tables(id)
                )
            """)
        conn.commit()
        conn.close()
    except Exception:
        pass

def add_notification(title, message, type="info", role=None, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (user_id, role, title, message, type, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, role, title, message, type, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_notifications(role=None, user_id=None, limit=20):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute(
            "SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
            (user_id, limit)
        )
    elif role:
        cursor.execute(
            "SELECT * FROM notifications WHERE role = ? OR role IS NULL ORDER BY created_at DESC LIMIT ?",
            (role, limit)
        )
    else:
        cursor.execute(
            "SELECT * FROM notifications ORDER BY created_at DESC LIMIT ?", (limit,)
        )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def mark_notification_read(notification_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()

def unread_notification_count(role=None, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0", (user_id,))
    elif role:
        cursor.execute("SELECT COUNT(*) FROM notifications WHERE (role = ? OR role IS NULL) AND is_read = 0", (role,))
    else:
        cursor.execute("SELECT COUNT(*) FROM notifications WHERE is_read = 0")
    count = cursor.fetchone()[0]
    conn.close()
    return count

if __name__ == "__main__":
    init_db()
    migrate_db()
    print("Database initialized at:", DB_FILE)
