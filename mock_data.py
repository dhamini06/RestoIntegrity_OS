import sqlite3
import json
from datetime import datetime, timedelta
from database import get_db_connection, init_db, migrate_db
from security import hash_password

def seed_db():
    init_db()
    migrate_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    now_str = datetime.now().isoformat()

    if user_count == 0:
        users_data = [
            ('dhamini467@gmail.com', hash_password('Dhamini@123'), 'K. Dhamini', 'admin', None, None, 0, now_str, now_str),
            ('admin@resto.com', hash_password('admin123'), 'Admin User', 'admin', None, None, 0, now_str, now_str),
            ('alice@resto.com', hash_password('alice123'), 'Alice Server', 'staff', None, None, 0, now_str, now_str),
            ('bob@resto.com', hash_password('bob123'), 'Bob Server', 'staff', None, None, 0, now_str, now_str),
            ('charlie@resto.com', hash_password('charlie123'), 'Charlie Server', 'staff', None, None, 0, now_str, now_str),
            ('chef@resto.com', hash_password('chef123'), 'Chef Ramsay', 'kitchen', None, None, 0, now_str, now_str),
            ('guest@resto.com', hash_password('guest123'), 'Walk-in Guest', 'customer', None, None, 0, now_str, now_str),
        ]
        cursor.executemany(
            "INSERT INTO users (email, password_hash, full_name, role, avatar_url, google_id, email_verified, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            users_data
        )

    cursor.execute("SELECT COUNT(*) FROM restaurant_tables")
    if cursor.fetchone()[0] == 0:
        tables_data = [
            ("Table 1", 2, "Window"),
            ("Table 2", 4, "Main Hall"),
            ("Table 3", 2, "Main Hall"),
            ("Table 4", 6, "Window"),
            ("Table 5", 4, "Patio"),
            ("Table 6", 2, "Patio"),
            ("Table 7", 8, "VIP Room"),
            ("Table 8", 4, "Main Hall"),
        ]
        cursor.executemany(
            "INSERT INTO restaurant_tables (table_number, capacity, location) VALUES (?, ?, ?)",
            tables_data
        )

    cursor.execute("SELECT id, email, full_name FROM users LIMIT 10")
    user_map = {r["email"]: r for r in cursor.fetchall()}

    cursor.execute("SELECT COUNT(*) FROM menu_items")
    if cursor.fetchone()[0] == 0:
        menu_items_data = [
            ('Truffle Fries', 'Crispy russet fries tossed in truffle oil and parmesan cheese.', 12.0, 'Starter', 1, 50),
            ('Spicy Miso Ramen', 'Rich pork broth with miso paste, wavy noodles, and chashu pork.', 18.0, 'Main', 1, 40),
            ('Wagyu Ribeye', 'A5 Miyazaki Wagyu ribeye steak (250g) grilled to perfection.', 45.0, 'Main', 1, 15),
            ('Lava Cake', 'Decadent chocolate cake with a molten fudge core, served with vanilla ice cream.', 10.0, 'Dessert', 1, 20),
            ('Iced Matcha Latte', 'Premium Japanese matcha whisked with cold milk and sweet cane syrup.', 6.0, 'Beverage', 1, 60),
            ('Craft IPA Beer', 'Local double dry-hopped IPA with notes of citrus and pine.', 8.0, 'Beverage', 1, 35)
        ]
        cursor.executemany(
            "INSERT INTO menu_items (name, description, price, category, is_available, stock_level) VALUES (?, ?, ?, ?, ?, ?)",
            menu_items_data
        )

    cursor.execute("SELECT COUNT(*) FROM inventory")
    if cursor.fetchone()[0] == 0:
        inventory_data = [
            ('Potatoes', 25.0, 5.0, 'kg', now_str),
            ('Ramen Noodles', 15.0, 3.0, 'kg', now_str),
            ('Wagyu Ribeye Cut', 12.0, 2.0, 'kg', now_str),
            ('Chocolate Lava Batter', 5.0, 1.0, 'kg', now_str),
            ('Matcha Powder', 2.0, 0.5, 'kg', now_str),
            ('Keg Beer', 50.0, 10.0, 'liters', now_str)
        ]
        cursor.executemany(
            "INSERT INTO inventory (item_name, current_quantity, min_threshold, unit, last_updated) VALUES (?, ?, ?, ?, ?)",
            inventory_data
        )

    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        base_time = datetime(2026, 7, 23, 12, 0, 0)
        staff_emails = ["alice@resto.com", "bob@resto.com", "charlie@resto.com"]

        order_scenarios = [
            (timedelta(hours=2), "Table 4", "completed", [(1, 2, 12.0), (5, 2, 6.0)], 0.0, None, staff_emails[0], "Card", 0.18),
            (timedelta(hours=4), "Table 1", "completed", [(2, 1, 18.0), (6, 1, 8.0)], 0.0, None, staff_emails[1], "Cash", 0.20),
            (timedelta(hours=6), "Table 3", "completed", [(3, 2, 45.0), (6, 2, 8.0), (4, 1, 10.0)], 0.0, None, staff_emails[0], "Card", 0.22),
            (timedelta(hours=8), "Table 2", "completed", [(1, 1, 12.0), (4, 1, 10.0)], 0.0, None, staff_emails[1], "Mobile Pay", 0.15),
            (timedelta(hours=10), "Table 5", "voided", [(3, 1, 45.0), (6, 2, 8.0)], 0.0, None, staff_emails[1], "Cash", 0.0),
            (timedelta(hours=14), "Table 1", "completed", [(2, 2, 18.0), (5, 1, 6.0)], 0.0, None, staff_emails[0], "Card", 0.25),
            (timedelta(hours=18), "Table 3", "completed", [(3, 2, 45.0)], 45.0, staff_emails[0], staff_emails[0], "Cash", 0.20),
            (timedelta(hours=22), "Table 4", "completed", [(1, 1, 12.0), (2, 1, 18.0), (5, 2, 6.0)], 0.0, None, staff_emails[1], "Card", 0.18),
            (timedelta(hours=26), "Table 2", "completed", [(4, 2, 10.0), (5, 2, 6.0)], 0.0, None, staff_emails[2], "Mobile Pay", 0.20),
            (timedelta(hours=30), "Table 5", "completed", [(3, 1, 45.0), (6, 1, 8.0)], 0.0, None, staff_emails[1], "Card", 0.22),
            (timedelta(hours=32), "Table 1", "voided", [(1, 2, 12.0), (5, 1, 6.0)], 0.0, None, staff_emails[1], "Cash", 0.0),
            (timedelta(hours=36), "Table 3", "completed", [(2, 2, 18.0), (4, 2, 10.0)], 0.0, None, staff_emails[0], "Card", 0.20),
            (timedelta(hours=40), "Table 4", "completed", [(3, 1, 45.0), (6, 3, 8.0)], 0.0, None, staff_emails[0], "Cash", 0.25),
            (timedelta(hours=44), "Table 2", "pending", [(2, 1, 18.0), (5, 1, 6.0)], 0.0, None, staff_emails[1], None, 0.0),
            (timedelta(hours=46), "Table 5", "preparing", [(3, 2, 45.0), (4, 2, 10.0)], 0.0, None, staff_emails[0], None, 0.0),
        ]

        for time_delta, table, status, items, discount, disc_by, served_by, pay_method, tip_pct in order_scenarios:
            o_time = (base_time + time_delta).isoformat()
            subtotal = sum(qty * price for _, qty, price in items)
            tax = round(subtotal * 0.0875, 2)
            tip = round(subtotal * tip_pct, 2) if status == 'completed' else 0.0
            total = round(subtotal - discount + tax + tip, 2)

            prepping_at = None
            completed_at = None
            if status in ('preparing', 'completed', 'voided'):
                prepping_at = (base_time + time_delta + timedelta(minutes=3)).isoformat()
            if status == 'completed':
                completed_at = (base_time + time_delta + timedelta(minutes=22)).isoformat()

            cursor.execute("""
                INSERT INTO orders (table_number, status, subtotal, discount, total, tax, tip,
                    payment_method, discount_applied_by, served_by, created_at, prepping_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (table, status, subtotal, discount, total, tax, tip,
                  pay_method, disc_by, served_by, o_time, prepping_at, completed_at))
            order_id = cursor.lastrowid

            for item_id, qty, price in items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                    (order_id, item_id, qty, price)
                )

        alerts_data = [
            (
                "void_anomaly", "high",
                json.dumps({
                    "table_number": "Table 5", "staff_username": "bob",
                    "order_total": 61.0,
                    "reason": "Order was marked void after being in preparing/cooking state for over 30 minutes.",
                    "timestamp": (datetime(2026, 7, 23, 23, 0) - timedelta(hours=38)).isoformat()
                }),
                "bob@resto.com",
                json.dumps({
                    "threat_classification": "High Cancellation Rate",
                    "risk_score": 85,
                    "incident_summary": "Order ID 5 (Table 5) was voided after kitchen started preparation.",
                    "recommended_actions": [
                        "Review the order lifecycle to understand why cancellation happened so late.",
                        "Confirm with the kitchen whether the Wagyu Ribeye ticket was completed.",
                        "Discuss void procedures with the staff member."
                    ]
                }),
                "active",
                (datetime(2026, 7, 23, 12, 0) + timedelta(hours=10)).isoformat()
            ),
            (
                "discount_anomaly", "medium",
                json.dumps({
                    "table_number": "Table 3", "staff_username": "alice",
                    "discount_amount": 45.0, "discount_percentage": 50.0,
                    "order_total": 90.0,
                    "reason": "An exceptionally high discount (50%) was manually applied without admin auth.",
                    "timestamp": (datetime(2026, 7, 23, 12, 0) + timedelta(hours=18)).isoformat()
                }),
                "alice@resto.com",
                json.dumps({
                    "threat_classification": "Unusual Discount Pattern",
                    "risk_score": 65,
                    "incident_summary": "A manual discount of 50% ($45.00) was applied on Table 3.",
                    "recommended_actions": [
                        "Verify if Table 3 was a VIP or authorized comp.",
                        "Review the staff member's discount frequency.",
                        "Consider requiring admin PIN entry for discounts over 20%."
                    ]
                }),
                "investigated",
                (datetime(2026, 7, 23, 12, 0) + timedelta(hours=18)).isoformat()
            ),
            (
                "shrinkage_anomaly", "medium",
                json.dumps({
                    "ingredient_name": "Wagyu Ribeye Cut",
                    "calculated_usage": "2.5 kg (based on 5 steaks sold)",
                    "actual_usage": "4.5 kg (based on physical count)",
                    "discrepancy": "2.0 kg missing (approx. 4 ribeye cuts)",
                    "timestamp": (datetime(2026, 7, 23, 12, 0) + timedelta(hours=36)).isoformat()
                }),
                None,
                json.dumps({
                    "threat_classification": "Stock Depletion Warning",
                    "risk_score": 70,
                    "incident_summary": "Reconciliation check detected a 2.0 kg discrepancy in Wagyu Ribeye Cut inventory.",
                    "recommended_actions": [
                        "Check with chef if any Wagyu steaks were discarded without logging.",
                        "Audit portion controls to ensure steaks match the 250g specification.",
                        "Run daily spot inventory counts on high-value items."
                    ]
                }),
                "active",
                (datetime(2026, 7, 23, 12, 0) + timedelta(hours=36)).isoformat()
            )
        ]

        cursor.executemany(
            "INSERT INTO security_alerts (alert_type, severity, details, triggered_by, ai_analysis, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            alerts_data
        )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_db()
    print("Database seeded successfully.")
