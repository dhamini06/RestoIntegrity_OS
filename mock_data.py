import sqlite3
import json
from datetime import datetime, timedelta
from database import get_db_connection, init_db

def seed_db():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if we already have data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print("Database already has data. Skipping seed.")
        conn.close()
        return

    print("Seeding database with rich mock data...")
    
    # 1. Seed Users
    users_data = [
        ('admin', 'admin123', 'admin', 'Dhamini Admin'),
        ('alice', 'alice123', 'staff', 'Alice Server'),
        ('bob', 'bob123', 'staff', 'Bob Server'),
        ('chef_ramsay', 'chef123', 'kitchen', 'Chef Ramsay'),
        ('guest', 'guest123', 'customer', 'Walk-in Guest')
    ]
    cursor.executemany(
        "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
        users_data
    )
    
    # 2. Seed Menu Items
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
    
    # 3. Seed Inventory
    now_str = datetime.now().isoformat()
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
    
    # 4. Seed Historical Orders (Last 48 hours for analytics)
    # We will generate orders at random intervals
    base_time = datetime.now() - timedelta(days=2)
    
    orders = []
    # Create ~15 realistic orders
    order_scenarios = [
        # time_delta, table, status, items (item_id, qty, price), discount, staff
        (timedelta(hours=2), "Table 4", "completed", [(1, 2, 12.0), (5, 2, 6.0)], 0.0, "alice"),
        (timedelta(hours=4), "Table 1", "completed", [(2, 1, 18.0), (6, 1, 8.0)], 0.0, "bob"),
        (timedelta(hours=6), "Table 3", "completed", [(3, 2, 45.0), (6, 2, 8.0), (4, 1, 10.0)], 0.0, "alice"),
        (timedelta(hours=8), "Table 2", "completed", [(1, 1, 12.0), (4, 1, 10.0)], 0.0, "bob"),
        # Suspicious void order
        (timedelta(hours=10), "Table 5", "voided", [(3, 1, 45.0), (6, 2, 8.0)], 0.0, "bob"), 
        (timedelta(hours=14), "Table 1", "completed", [(2, 2, 18.0), (5, 1, 6.0)], 0.0, "alice"),
        # Suspicious discount order
        (timedelta(hours=18), "Table 3", "completed", [(3, 2, 45.0)], 45.0, "alice"), # 50% discount
        (timedelta(hours=22), "Table 4", "completed", [(1, 1, 12.0), (2, 1, 18.0), (5, 2, 6.0)], 0.0, "bob"),
        (timedelta(hours=26), "Table 2", "completed", [(4, 2, 10.0), (5, 2, 6.0)], 0.0, "alice"),
        (timedelta(hours=30), "Table 5", "completed", [(3, 1, 45.0), (6, 1, 8.0)], 0.0, "bob"),
        # Another void order
        (timedelta(hours=32), "Table 1", "voided", [(1, 2, 12.0), (5, 1, 6.0)], 0.0, "bob"),
        (timedelta(hours=36), "Table 3", "completed", [(2, 2, 18.0), (4, 2, 10.0)], 0.0, "alice"),
        (timedelta(hours=40), "Table 4", "completed", [(3, 1, 45.0), (6, 3, 8.0)], 0.0, "alice"),
        (timedelta(hours=44), "Table 2", "pending", [(2, 1, 18.0), (5, 1, 6.0)], 0.0, "bob"),
        (timedelta(hours=46), "Table 5", "preparing", [(3, 2, 45.0), (4, 2, 10.0)], 0.0, "alice"),
    ]
    
    for time_delta, table, status, items, discount, staff in order_scenarios:
        o_time = (base_time + time_delta).isoformat()
        subtotal = sum(qty * price for _, qty, price in items)
        total = subtotal - discount
        
        cursor.execute(
            "INSERT INTO orders (table_number, status, subtotal, discount, total, discount_applied_by, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (table, status, subtotal, discount, total, staff if discount > 0 else None, o_time)
        )
        order_id = cursor.lastrowid
        
        for item_id, qty, price in items:
            cursor.execute(
                "INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                (order_id, item_id, qty, price)
            )
            
    # 5. Seed Security Alerts
    alerts_data = [
        (
            "void_anomaly",
            "high",
            json.dumps({
                "table_number": "Table 5",
                "staff_username": "bob",
                "order_total": 61.0,
                "reason": "Order was marked void after being in preparing/cooking state for over 30 minutes. Order contained high-value item: Wagyu Ribeye.",
                "timestamp": (datetime.now() - timedelta(hours=38)).isoformat()
            }),
            "bob",
            json.dumps({
                "threat_classification": "Internal Cash Skimming (Suspicious Void)",
                "risk_score": 85,
                "incident_summary": "Order ID 5 (Table 5) was marked as voided by Bob after the kitchen started preparation. Since the kitchen had processed the order, food was likely served. Voiding the order afterwards is a common pattern for pocketing cash payments.",
                "recommended_actions": [
                    "Perform a spot check of Table 5 CCTV footage around the void timestamp.",
                    "Verify with the kitchen if the Wagyu Ribeye ticket was completed and served.",
                    "Review Bob's cash drawer balance at the end of the shift."
                ]
            }),
            "active",
            (datetime.now() - timedelta(hours=38)).isoformat()
        ),
        (
            "discount_anomaly",
            "medium",
            json.dumps({
                "table_number": "Table 3",
                "staff_username": "alice",
                "discount_amount": 45.0,
                "discount_percentage": 50.0,
                "order_total": 90.0,
                "reason": "An exceptionally high discount (50%) was manually applied by Alice without admin auth log verification.",
                "timestamp": (datetime.now() - timedelta(hours=30)).isoformat()
            }),
            "alice",
            json.dumps({
                "threat_classification": "Unauthorized Employee Discount Abuse",
                "risk_score": 65,
                "incident_summary": "A manual discount of 50% ($45.00) was applied by Alice on Table 3. There is no supervisor override authorization recorded for this transaction, which exceeds the standard staff discount policy limit of 15%.",
                "recommended_actions": [
                    "Verify if Table 3 guests were authorized for VIP discounts.",
                    "Audit Alice's discount frequency to check if this is a recurring behavior.",
                    "Implement a hard restriction forcing admin PIN entry for discounts > 20%."
                ]
            }),
            "investigated",
            (datetime.now() - timedelta(hours=30)).isoformat()
        ),
        (
            "shrinkage_anomaly",
            "medium",
            json.dumps({
                "ingredient_name": "Wagyu Ribeye Cut",
                "calculated_usage": "2.5 kg (based on 5 steaks sold)",
                "actual_usage": "4.5 kg (based on physical count)",
                "discrepancy": "2.0 kg missing (approx. 4 ribeye cuts)",
                "timestamp": (datetime.now() - timedelta(hours=12)).isoformat()
            }),
            None,
            json.dumps({
                "threat_classification": "Inventory Shrinkage (High Discrepancy)",
                "risk_score": 70,
                "incident_summary": "Reconciliation check detected a 2.0 kg (approx. 4 servings) discrepancy in Wagyu Ribeye Cut inventory. Sold quantity accounts for 2.5 kg, but 4.5 kg was depleted from stock, suggesting unrecorded waste or kitchen theft.",
                "recommended_actions": [
                    "Ask the chef if any Wagyu steaks were spoiled or discarded as waste without logging.",
                    "Verify portion controls in the kitchen to ensure steaks do not exceed 250g specification.",
                    "Audit freezer access logs if lock sensors are active."
                ]
            }),
            "active",
            (datetime.now() - timedelta(hours=12)).isoformat()
        )
    ]
    
    cursor.executemany(
        "INSERT INTO security_alerts (alert_type, severity, details, triggered_by, ai_analysis, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        alerts_data
    )
    
    conn.commit()
    conn.close()
    print("Database seeded successfully.")

if __name__ == "__main__":
    seed_db()
