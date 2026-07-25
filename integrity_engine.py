import sqlite3
import json
from datetime import datetime
from database import get_db_connection
from gemini_service import investigate_alert_with_gemini

def log_security_alert(alert_type, severity, details_dict, triggered_by=None):
    """
    Saves a security alert to the DB and triggers a background Gemini investigation.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now_str = datetime.now().isoformat()
    details_json = json.dumps(details_dict)
    
    cursor.execute(
        "INSERT INTO security_alerts (alert_type, severity, details, triggered_by, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (alert_type, severity, details_json, triggered_by, 'active', now_str)
    )
    alert_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Trigger Gemini analysis (or offline fallback) for the newly created alert
    try:
        investigate_alert_with_gemini(alert_id)
    except Exception as e:
        print(f"[Integrity Engine] Warning: Gemini investigation failed: {e}")
        
    return alert_id

def check_void_anomaly(order_id, staff_username, current_status):
    """
    Checks if voiding a completed or preparing order is a potential cash skimming attempt.
    """
    if current_status not in ['preparing', 'completed']:
        return None
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_number, total FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    conn.close()
    
    if not order:
        return None
        
    details = {
        "order_id": order_id,
        "table_number": order['table_number'],
        "staff_username": staff_username,
        "order_total": order['total'],
        "reason": f"Order was marked void after being in '{current_status}' state. Prepared food was likely served, suggesting pocketed cash.",
        "timestamp": datetime.now().isoformat()
    }
    
    alert_id = log_security_alert(
        alert_type="void_anomaly",
        severity="high",
        details_dict=details,
        triggered_by=staff_username
    )
    return alert_id

def check_discount_anomaly(order_id, staff_username, discount_amount):
    """
    Checks if the manually applied discount is suspicious (> 30% of subtotal).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT table_number, subtotal FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    conn.close()
    
    if not order or order['subtotal'] <= 0:
        return None
        
    subtotal = order['subtotal']
    discount_pct = (discount_amount / subtotal) * 100
    
    if discount_pct >= 30.0:
        details = {
            "order_id": order_id,
            "table_number": order['table_number'],
            "staff_username": staff_username,
            "discount_amount": discount_amount,
            "discount_percentage": round(discount_pct, 1),
            "reason": f"High manual discount ({round(discount_pct, 1)}%) applied by staff without admin supervisor log.",
            "timestamp": datetime.now().isoformat()
        }
        
        alert_id = log_security_alert(
            alert_type="discount_anomaly",
            severity="medium",
            details_dict=details,
            triggered_by=staff_username
        )
        return alert_id
    return None

def check_shrinkage_anomaly(ingredient_name, physical_qty, staff_username=None):
    """
    Reconciles theoretical inventory levels (previous_qty - calculated sales consumption)
    with actual physical count reports.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT current_quantity, unit FROM inventory WHERE item_name = ?", (ingredient_name,))
    inv = cursor.fetchone()
    conn.close()
    
    if not inv:
        return None
        
    theoretical_qty = inv['current_quantity']
    discrepancy = theoretical_qty - physical_qty
    
    # If discrepancy is positive and significant (e.g., > 10% of standard stock or > 1kg/unit)
    if discrepancy > 0.5:
        details = {
            "ingredient_name": ingredient_name,
            "theoretical_quantity": theoretical_qty,
            "physical_quantity": physical_qty,
            "discrepancy": round(discrepancy, 2),
            "unit": inv['unit'],
            "reason": f"Physical count reported {round(discrepancy, 2)} {inv['unit']} lower than expected inventory stock level.",
            "timestamp": datetime.now().isoformat()
        }
        
        alert_id = log_security_alert(
            alert_type="shrinkage_anomaly",
            severity="medium" if discrepancy < 3.0 else "high",
            details_dict=details,
            triggered_by=staff_username
        )
        return alert_id
    return None
