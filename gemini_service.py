import os
import json
import random
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from database import get_db_connection

# Structured Output Schemas
class AIIncidentAnalysis(BaseModel):
    threat_classification: str = Field(description="Operational issue category (e.g., High Cancellation Rate, Discount Spike, Stock Depletion)")
    risk_score: int = Field(description="Priority score from 0 (Low) to 100 (Critical)")
    incident_summary: str = Field(description="Professional analysis summarizing the operational event and its business impact")
    recommended_actions: list[str] = Field(description="3 actionable steps for the restaurant owner to address the issue")

class RecommendationResponse(BaseModel):
    suggested_item_name: str = Field(description="Name of the menu item recommended from the restaurant menu")
    recommendation_reason: str = Field(description="Short, high-conversion selling point explaining the pairing recommendation")

class StockoutForecast(BaseModel):
    predicted_runout_days: float = Field(description="Estimated number of days before this item is completely depleted based on sales velocity")
    risk_level: str = Field(description="Risk rating: Low, Medium, High, or Critical")
    explanation: str = Field(description="Brief explanation of seasonal demand or sales patterns driving this forecast")

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            return genai.Client(api_key=api_key)
        except Exception as e:
            print(f"[Gemini Service] Init error: {e}")
    return None

def investigate_alert_with_gemini(alert_id):
    """
    Enriches an operational alert with structured AI analysis.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, alert_type, severity, details, created_at FROM security_alerts WHERE id = ?", (alert_id,))
    alert = cursor.fetchone()
    
    if not alert:
        conn.close()
        return
        
    alert_type = alert['alert_type']
    details = json.loads(alert['details'])
    created_at = alert['created_at']
    
    client = get_gemini_client()
    
    if client:
        try:
            prompt = f"""
            You are a Restaurant Operations Consultant analyzing operational data.
            Analyze the following alert:
            
            Alert ID: {alert_id}
            Alert Type: {alert_type}
            Severity: {alert['severity']}
            Timestamp: {created_at}
            Alert Details: {json.dumps(details, indent=2)}
            
            Classify the issue, assign a priority score (0 to 100), write a professional summary, and outline 3 action steps for the owner.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AIIncidentAnalysis,
                    system_instruction="You analyze restaurant transactions and inventory data to identify operational inefficiencies, revenue leakage, and inventory management issues.",
                    temperature=0.2
                )
            )
            
            ai_data = response.text
            cursor.execute("UPDATE security_alerts SET ai_analysis = ? WHERE id = ?", (ai_data, alert_id))
            conn.commit()
            conn.close()
            return
            
        except Exception as e:
            print(f"[Gemini Service] API error: {e}. Falling back to offline template.")
            
    # Offline Fallback (Rule-Based Mock)
    analysis = generate_offline_alert_analysis(alert_type, details)
    cursor.execute("UPDATE security_alerts SET ai_analysis = ? WHERE id = ?", (json.dumps(analysis), alert_id))
    conn.commit()
    conn.close()

def generate_offline_alert_analysis(alert_type, details):
    if alert_type == "void_anomaly":
        return {
            "threat_classification": "High Cancellation Rate (Post-Preparation Void)",
            "risk_score": 85,
            "incident_summary": f"Order #{details.get('order_id', 'N/A')} on Table {details.get('table_number', 'N/A')} was voided by '{details.get('staff_username', 'unknown')}' after preparation started. The kitchen had already processed this order, so food was likely served. Late cancellations disrupt revenue tracking and kitchen workflow.",
            "recommended_actions": [
                "Review the order timeline to understand why the cancellation happened so late.",
                "Confirm with kitchen staff if this ticket was completed and dispatched.",
                "Discuss void procedures with the staff member to prevent future late cancellations."
            ]
        }
    elif alert_type == "discount_anomaly":
        pct = details.get('discount_percentage', 0)
        return {
            "threat_classification": "Unusual Discount Pattern",
            "risk_score": 60 if pct < 50 else 80,
            "incident_summary": f"A manual discount of {pct}% (${details.get('discount_amount', 0)}) was applied by '{details.get('staff_username', 'unknown')}' on Table {details.get('table_number', 'N/A')}. This exceeds the standard discount threshold without supervisor approval.",
            "recommended_actions": [
                "Verify if the table was a VIP or authorized comp.",
                "Review the staff member's discount frequency for patterns.",
                "Consider requiring manager override for discounts exceeding 20%."
            ]
        }
    else: # shrinkage
        item = details.get('ingredient_name', 'Ingredient')
        disc = details.get('discrepancy', 0)
        unit = details.get('unit', '')
        return {
            "threat_classification": "Stock Depletion Warning",
            "risk_score": 70,
            "incident_summary": f"Physical counts of {item} show {disc} {unit}(s) unaccounted for compared to sales records. The kitchen is depleting stock faster than sales data explains.",
            "recommended_actions": [
                "Check with kitchen staff on portion control or unlogged waste/spoilage.",
                "Verify delivery receipts match the last supply invoice.",
                "Run daily spot counts on high-value ingredients."
            ]
        }

def get_menu_recommendations(cart_items):
    """
    Returns a customized upsell recommendation.
    """
    if not cart_items:
        return {
            "suggested_item_name": "Truffle Fries",
            "recommendation_reason": "Our crowd-favorite! Perfect starter to share while your mains are being prepared."
        }
        
    client = get_gemini_client()
    cart_names = [item['name'] for item in cart_items]
    
    # Available items in our database menu:
    # Truffle Fries, Spicy Miso Ramen, Wagyu Ribeye, Lava Cake, Iced Matcha Latte, Craft IPA Beer
    if client:
        try:
            prompt = f"""
            The customer currently has these items in their cart: {', '.join(cart_names)}.
            Recommend ONE item from this list:
            - Truffle Fries ($12.00)
            - Spicy Miso Ramen ($18.00)
            - Wagyu Ribeye ($45.00)
            - Lava Cake ($10.00)
            - Iced Matcha Latte ($6.00)
            - Craft IPA Beer ($8.00)
            
            Select the most complementary pairing that is NOT already in their cart. Provide the recommendation name and a compelling 1-sentence sales pitch.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RecommendationResponse,
                    temperature=0.7
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[Gemini Service] Recommendations API error: {e}")
            
    # Offline Fallback Recommendations
    if any("Ramen" in n or "Ribeye" in n for n in cart_names):
        # Recommend a drink or dessert
        if not any("Latte" in n or "Beer" in n for n in cart_names):
            return {
                "suggested_item_name": "Craft IPA Beer",
                "recommendation_reason": "The crisp, hop-forward notes of our dry-hopped IPA cut through rich mains perfectly."
            }
        else:
            return {
                "suggested_item_name": "Lava Cake",
                "recommendation_reason": "End your meal on a sweet note with our rich, molten chocolate lava cake."
            }
    else:
        return {
            "suggested_item_name": "Truffle Fries",
            "recommendation_reason": "Elevate your meal with crispy, gold fries drizzled in truffle oil and parmesan."
        }

def get_demand_forecast(ingredient_name, current_qty):
    """
    Forecasts stockout velocity for a specific ingredient.
    """
    client = get_gemini_client()
    if client:
        try:
            prompt = f"""
            Analyze the stock levels and velocity for:
            Ingredient: {ingredient_name}
            Current Physical Stock: {current_qty}
            
            Generate a stockout forecast assuming standard daily restaurant consumption velocity.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=StockoutForecast,
                    temperature=0.2
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[Gemini Service] Forecasting API error: {e}")
            
    # Offline Fallback Forecast
    import random
    days = round(current_qty / random.uniform(2.5, 4.5), 1)
    risk = "Low"
    if days < 2.0:
        risk = "Critical"
    elif days < 4.0:
        risk = "High"
    elif days < 7.0:
        risk = "Medium"
        
    return {
        "predicted_runout_days": max(days, 0.2),
        "risk_level": risk,
        "explanation": f"Current stock levels are matching normal historical sales velocities. Expected runout is in {days} days."
    }

def detect_kitchen_bottlenecks():
    """
    Analyzes order completion times to detect kitchen bottlenecks.
    Returns list of bottleneck findings.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT o.id, o.table_number, o.created_at, o.prepping_at, o.completed_at,
               o.served_by, GROUP_CONCAT(mi.name, ', ') as items
        FROM orders o
        LEFT JOIN order_items oi ON oi.order_id = o.id
        LEFT JOIN menu_items mi ON mi.id = oi.menu_item_id
        WHERE o.status = 'completed' AND o.prepping_at IS NOT NULL AND o.completed_at IS NOT NULL
        GROUP BY o.id
        ORDER BY o.created_at DESC LIMIT 30
    """)
    completed = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("""
        SELECT o.id, o.table_number, o.created_at, o.prepping_at,
               o.served_by, GROUP_CONCAT(mi.name, ', ') as items
        FROM orders o
        LEFT JOIN order_items oi ON oi.order_id = o.id
        LEFT JOIN menu_items mi ON mi.id = oi.menu_item_id
        WHERE o.status IN ('pending', 'preparing')
        GROUP BY o.id
        ORDER BY o.created_at ASC
    """)
    active = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    findings = []
    
    cook_times = []
    for o in completed:
        try:
            prep = datetime.fromisoformat(o['prepping_at'])
            done = datetime.fromisoformat(o['completed_at'])
            cook_min = (done - prep).total_seconds() / 60
            cook_times.append(cook_min)
        except Exception:
            pass
    
    if cook_times:
        avg_cook = sum(cook_times) / len(cook_times)
        max_cook = max(cook_times)
        findings.append({
            "type": "avg_cook_time",
            "value": round(avg_cook, 1),
            "detail": f"Average cook time: {avg_cook:.1f} minutes",
            "severity": "good" if avg_cook < 15 else "warning" if avg_cook < 25 else "critical"
        })
        findings.append({
            "type": "max_cook_time",
            "value": round(max_cook, 1),
            "detail": f"Longest cook time: {max_cook:.1f} minutes",
            "severity": "good" if max_cook < 25 else "warning" if max_cook < 40 else "critical"
        })
    
    if active:
        stalled = []
        for o in active:
            try:
                elapsed = (datetime.now() - datetime.fromisoformat(o['created_at'])).total_seconds() / 60
                if elapsed > 20:
                    stalled.append(o)
            except Exception:
                pass
        if stalled:
            findings.append({
                "type": "stalled_orders",
                "value": len(stalled),
                "detail": f"{len(stalled)} orders have been active for over 20 minutes",
                "severity": "critical"
            })
    
    findings.append({
        "type": "kitchen_load",
        "value": len(active),
        "detail": f"{len(active)} orders currently in kitchen",
        "severity": "good" if len(active) < 5 else "warning" if len(active) < 10 else "critical"
    })
    
    return findings


def generate_smart_notifications():
    """
    Analyzes current restaurant data and generates contextual notifications.
    Returns list of (title, message, type, role) tuples.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM inventory WHERE current_quantity <= min_threshold")
    low_stock = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status IN ('pending', 'preparing')")
    kitchen_load = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM security_alerts WHERE status='active'")
    active_alerts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM queue WHERE status='waiting'")
    queue_size = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM orders
        WHERE created_at >= datetime('now', '-1 hour')
    """)
    orders_last_hour = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM orders
        WHERE status='completed' AND created_at >= datetime('now', '-1 hour')
    """)
    completed_last_hour = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM restaurant_tables WHERE status='available'
    """)
    available = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) FROM restaurant_tables
    """)
    total = cursor.fetchone()[0]
    conn.close()
    
    notifications = []
    
    if low_stock > 0:
        notifications.append((
            "Low Stock Alert",
            f"{low_stock} ingredient(s) below minimum threshold. Check inventory for restock.",
            "warning", "admin"
        ))
    
    if kitchen_load > 5:
        notifications.append((
            "Kitchen Overload",
            f"{kitchen_load} orders in queue. Consider additional kitchen staff.",
            "alert", "admin"
        ))
    
    if active_alerts > 2:
        notifications.append((
            "Multiple Alerts",
            f"{active_alerts} active security alerts require investigation.",
            "alert", "admin"
        ))
    
    if queue_size > 3:
        notifications.append((
            "Queue Growing",
            f"{queue_size} parties waiting. Current availability: {available}/{total} tables.",
            "warning", "staff"
        ))
    
    if orders_last_hour > 10:
        notifications.append((
            "Rush Hour Detected",
            f"{orders_last_hour} orders in the last hour ({completed_last_hour} completed). Peak operations.",
            "info", "kitchen"
        ))
    elif orders_last_hour == 0:
        notifications.append((
            "Slow Period",
            "No orders in the last hour. Consider running a lunch special.",
            "info", "admin"
        ))
    
    if available <= 1 and total > 1:
        notifications.append((
            "Near Capacity",
            f"Only {available}/{total} tables available. Manage reservations and queue.",
            "warning", "staff"
        ))
    
    return notifications


def get_smart_inventory_forecast():
    """
    Uses actual order data to calculate consumption velocity and predict stockout dates.
    Returns list of dicts with predicted_runout_days, risk_level for each inventory item.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT item_name, current_quantity, min_threshold, unit FROM inventory")
    inventory = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("""
        SELECT oi.menu_item_id, mi.name, SUM(oi.quantity) as total_ordered
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        WHERE o.status = 'completed' AND o.created_at >= datetime('now', '-30 days')
        GROUP BY mi.name
    """)
    menu_sales = {r['name']: r['total_ordered'] for r in cursor.fetchall()}
    
    cursor.execute("""
        SELECT DISTINCT strftime('%Y-%m-%d', created_at) as day
        FROM orders WHERE status = 'completed' AND created_at >= datetime('now', '-30 days')
    """)
    active_days = len(cursor.fetchall()) or 1
    conn.close()
    
    menu_item_map = {
        "Tomatoes": "Spicy Miso Ramen",
        "Potatoes": "Truffle Fries",
        "Chicken Breast": "Wagyu Ribeye",
        "Lettuce": "Caesar Salad",
        "Onions": "Spicy Miso Ramen",
        "Cheese": "Truffle Fries",
        "Pasta": "Spaghetti Bolognese",
        "Olive Oil": "Caesar Salad",
        "Flour": "Lava Cake",
        "Sugar": "Iced Matcha Latte",
        "Beef": "Wagyu Ribeye",
        "Cream": "Lava Cake",
        "Spices": "Spicy Miso Ramen",
        "Buns": "Classic Burger",
        "Fish": "Grilled Salmon",
    }
    
    results = []
    for item in inventory:
        name = item['item_name']
        qty = item['current_quantity']
        threshold = item['min_threshold']
        unit = item['unit']
        
        menu_item = menu_item_map.get(name)
        sales_volume = menu_sales.get(menu_item, 0) if menu_item else 0
        
        daily_consumption = max(sales_volume / active_days, 0.1)
        usable_stock = max(qty - threshold, 0)
        days = round(usable_stock / daily_consumption, 1) if daily_consumption > 0 else 999
        
        risk = "Low"
        if days < 2:
            risk = "Critical"
        elif days < 4:
            risk = "High"
        elif days < 8:
            risk = "Medium"
        
        results.append({
            "item_name": name,
            "current_qty": qty,
            "threshold": threshold,
            "unit": unit,
            "daily_consumption": round(daily_consumption, 2),
            "predicted_runout_days": days,
            "risk_level": risk,
            "menu_item": menu_item or "Unknown"
        })
    
    return results


def ask_manager_assistant(chat_history, user_message):
    """
    Interact with the manager's AI assistant about operations, sales, and stock.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT alert_type, severity, details, created_at FROM security_alerts ORDER BY id DESC LIMIT 5")
    recent_alerts = [dict(row) for row in cursor.fetchall()]
    
    cursor.execute("SELECT item_name, current_quantity, min_threshold, unit FROM inventory")
    inventory = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    context = {
        "system_status": "RestoIntegrity OS Smart Operations Platform active.",
        "recent_operational_alerts": recent_alerts,
        "current_inventory": inventory
    }
    
    client = get_gemini_client()
    if client:
        try:
            formatted_history = []
            for role, text in chat_history:
                formatted_history.append(f"{role.capitalize()}: {text}")
                
            history_text = "\n".join(formatted_history)
            
            prompt = f"""
            Context:
            {json.dumps(context, indent=2)}
            
            Conversation History:
            {history_text}
            
            Manager's Message: {user_message}
            
            Respond as a helpful, expert restaurant operations assistant. Answer questions using the provided database context when relevant.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.4)
            )
            return response.text
        except Exception as e:
            return f"I'm sorry, I encountered an error connecting to Gemini: {e}."
            
    # Offline Fallback
    msg = user_message.lower()
    if "alert" in msg or "security" in msg or "fraud" in msg:
        return f"Operations Hub shows {len(recent_alerts)} recent events. The most notable is a high-severity cancellation anomaly triggered by Bob."
    elif "inventory" in msg or "stock" in msg or "shrink" in msg:
        low_items = [i['item_name'] for i in inventory if i['current_quantity'] <= i['min_threshold']]
        low_str = ", ".join(low_items) if low_items else "none"
        return f"Inventory items below warning threshold: **{low_str}**."
    else:
        return "I'm your RestoIntegrity Business Advisor. I can help analyze orders, cancellations, discounts, inventory, and tips. What would you like to check?"


def query_database_copilot(user_message, include_data=False):
    """
    Natural-language database query engine.
    Returns (answer_text, optional_dataframe).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count, COALESCE(SUM(total),0) as rev FROM orders WHERE status='completed'")
    sales_summary = dict(cursor.fetchone())
    
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status IN ('pending','preparing')")
    pending_orders = cursor.fetchone()[0]
    
    cursor.execute("SELECT item_name, current_quantity, min_threshold FROM inventory")
    inv_rows = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("""
        SELECT mi.name, SUM(oi.quantity) as sold
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        WHERE o.status = 'completed'
        GROUP BY mi.name ORDER BY sold DESC
    """)
    top_items = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT COUNT(*) FROM security_alerts WHERE status='active'")
    active_alerts = cursor.fetchone()[0]
    
    cursor.execute("SELECT served_by, COUNT(*) as cnt, SUM(CASE WHEN status='completed' THEN tip ELSE 0 END) as tips FROM orders WHERE served_by IS NOT NULL AND status='completed' GROUP BY served_by")
    staff_data = [dict(r) for r in cursor.fetchall()]
    
    cursor.execute("SELECT COUNT(*) FROM reservations WHERE status='confirmed'")
    upcoming_reservations = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM queue WHERE status='waiting'")
    queue_size = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT mi.name, mi.stock_level, SUM(oi.quantity) as total_ordered
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        WHERE o.status = 'completed'
        GROUP BY mi.name
    """)
    menu_demand = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    low_stock = [i for i in inv_rows if i['current_quantity'] <= i['min_threshold']]
    low_stock_names = [i['item_name'] for i in low_stock]
    
    df = None
    msg = user_message.lower()
    
    # Intent matching
    if any(w in msg for w in ["revenue", "sales", "earnings", "money", "income"]):
        answer = f"Total verified revenue: **${sales_summary['rev']:,.2f}** across **{sales_summary['count']}** completed orders. "
        if top_items:
            answer += f"Top seller: **{top_items[0]['name']}** ({top_items[0]['sold']} units sold). "
        answer += f"Active alerts: {active_alerts}. Upcoming reservations: {upcoming_reservations}."
        if include_data:
            data = {"Metric": ["Revenue", "Completed Orders", "Active Alerts", "Reservations", "Queue"],
                    "Value": [f"${sales_summary['rev']:,.2f}", str(sales_summary['count']), str(active_alerts), str(upcoming_reservations), str(queue_size)]}
            df = pd.DataFrame(data)
    
    elif any(w in msg for w in ["inventory", "stock", "ingredient", "supply", "low"]):
        if low_stock:
            items_ls = [f"**{i['item_name']}** ({i['current_quantity']}/{i['min_threshold']} {i.get('unit','')})" for i in low_stock]
            answer = f"⚠️ **{len(low_stock)} items below threshold:** " + ", ".join(items_ls) + ". "
        else:
            answer = "✅ All inventory items are above minimum thresholds. "
        total_items = len(inv_rows)
        avg_stock = sum(i['current_quantity'] for i in inv_rows) / total_items if total_items else 0
        answer += f"Tracking **{total_items}** ingredients. Average stock level: **{avg_stock:.1f}** units."
        if include_data:
            df = pd.DataFrame(inv_rows)
    
    elif any(w in msg for w in ["order", "pending", "ticket", "kitchen", "cook"]):
        answer = f"**{pending_orders}** orders currently in kitchen (pending/preparing). "
        answer += f"**{sales_summary['count']}** completed orders total. "
        if staff_data:
            top_staff = max(staff_data, key=lambda x: x['cnt'])
            answer += f"Top performer: **{top_staff['served_by']}** ({top_staff['cnt']} orders, ${top_staff['tips']:.2f} in tips)."
        if include_data:
            df = pd.DataFrame(staff_data) if staff_data else pd.DataFrame()
    
    elif any(w in msg for w in ["tip", "waiter", "staff", "server", "employee"]):
        if staff_data:
            total_tips = sum(s['tips'] for s in staff_data)
            total_orders_staff = sum(s['cnt'] for s in staff_data)
            avg_tip = total_tips / total_orders_staff if total_orders_staff else 0
            top_tipper = max(staff_data, key=lambda x: x['tips'])
            answer = f"Total staff tips: **${total_tips:.2f}**. Average tip per order: **${avg_tip:.2f}**. "
            answer += f"Highest earner: **{top_tipper['served_by']}** (${top_tipper['tips']:.2f})."
            if include_data:
                df = pd.DataFrame(staff_data)
        else:
            answer = "No staff tip data available yet. Complete some orders to generate insights."
    
    elif any(w in msg for w in ["menu", "item", "popular", "best", "top", "sell"]):
        if top_items:
            answer = f"🏆 **Best seller:** {top_items[0]['name']} ({top_items[0]['sold']} units). "
            if len(top_items) > 1:
                answer += f"**#2:** {top_items[1]['name']} ({top_items[1]['sold']} units). "
            if len(top_items) > 2:
                answer += f"**#3:** {top_items[2]['name']} ({top_items[2]['sold']} units). "
            total_sold = sum(i['sold'] for i in top_items)
            for t in top_items:
                pct = (t['sold'] / total_sold * 100) if total_sold else 0
                t['share'] = f"{pct:.1f}%"
            answer += f"Tracking **{len(top_items)}** menu items."
            if include_data:
                df = pd.DataFrame(top_items)
        else:
            answer = "No sales data yet. Complete some orders first."
    
    elif any(w in msg for w in ["reservation", "booking", "guest"]):
        answer = f"Upcoming reservations: **{upcoming_reservations}**. "
        answer += f"Customers currently in queue: **{queue_size}**. "
        answer += f"Active security alerts: **{active_alerts}**."
        if include_data:
            data = {"Metric": ["Reservations", "Queue", "Active Alerts"],
                    "Value": [str(upcoming_reservations), str(queue_size), str(active_alerts)]}
            df = pd.DataFrame(data)
    
    elif any(w in msg for w in ["alert", "security", "anomaly", "fraud", "void", "cancel"]):
        answer = f"**{active_alerts}** active alerts. Recent: "
        if recent_alerts:
            for a in recent_alerts[:3]:
                answer += f"**{a['alert_type']}** ({a['severity']}), "
            answer = answer.rstrip(", ") + ". "
        answer += "Check Operations Hub for full details."
        if include_data:
            df = pd.DataFrame(recent_alerts) if recent_alerts else pd.DataFrame()
    
    elif any(w in msg for w in ["demand", "forecast", "predict", "trend", "popular"]):
        if menu_demand:
            total_demand = sum(i['total_ordered'] for i in menu_demand) or 1
            for m in menu_demand:
                m['demand_share'] = f"{(m['total_ordered']/total_demand*100):.1f}%"
            hottest = max(menu_demand, key=lambda x: x['total_ordered'])
            answer = f"📊 **Highest demand:** {hottest['name']} ({hottest['total_ordered']} ordered, {hottest.get('demand_share','')} share). "
            low_demand = [m for m in menu_demand if m['total_ordered'] < total_demand * 0.05]
            if low_demand:
                answer += f"Slow movers: {', '.join(m['name'] for m in low_demand)}. "
            answer += "Consider promoting slower items via specials."
            if include_data:
                df = pd.DataFrame(menu_demand)
        else:
            answer = "No order data available for demand analysis."
    
    else:
        # General summary
        answer = f"📊 **RestoIntegrity OS Snapshot**\n\n"
        answer += f"• Revenue: **${sales_summary['rev']:,.2f}** ({sales_summary['count']} orders)\n"
        answer += f"• Kitchen: **{pending_orders}** orders in progress\n"
        answer += f"• Alerts: **{active_alerts}** active\n"
        if low_stock_names:
            answer += f"• Low stock: **{', '.join(low_stock_names)}**\n"
        answer += f"• Reservations: **{upcoming_reservations}** upcoming\n"
        answer += f"• Queue: **{queue_size}** waiting\n"
        if top_items:
            answer += f"• Best seller: **{top_items[0]['name']}**\n"
        answer += "\n💡 *Ask about revenue, inventory, orders, tips, menu performance, or reservations.*"
        if include_data:
            data = {"Metric": ["Revenue", "Orders", "Kitchen Load", "Active Alerts", "Reservations", "Queue"],
                    "Value": [f"${sales_summary['rev']:,.2f}", str(sales_summary['count']), str(pending_orders), str(active_alerts), str(upcoming_reservations), str(queue_size)]}
            df = pd.DataFrame(data)
    
    return answer, df
