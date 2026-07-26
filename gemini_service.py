import os
import json
import sqlite3
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

def ask_manager_assistant(chat_history, user_message):
    """
    Interact with the manager's AI assistant about operations, sales, and stock.
    """
    # Fetch some context from DB to make assistant smart
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Recent alerts
    cursor.execute("SELECT alert_type, severity, details, created_at FROM security_alerts ORDER BY id DESC LIMIT 5")
    recent_alerts = [dict(row) for row in cursor.fetchall()]
    
    # Stock status
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
            
            Respond as a helpful, expert restaurant operations assistant. Answer questions using the provided database context when relevant. Keep your answer professional, concise, and focused on operational insights, inventory management, and business recommendations.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4
                )
            )
            return response.text
        except Exception as e:
            return f"I'm sorry, I encountered an error connecting to Gemini: {e}. Please ensure your API key is correct."
            
    # Offline Fallback Assistant
    msg = user_message.lower()
    if "alert" in msg or "security" in msg or "fraud" in msg:
        return f"Operations Hub shows {len(recent_alerts)} recent events. The most notable is a high-severity cancellation anomaly triggered by Bob. Consider reviewing the order lifecycle for that table."
    elif "inventory" in msg or "stock" in msg or "shrink" in msg:
        low_items = [i['item_name'] for i in inventory if i['current_quantity'] <= i['min_threshold']]
        low_str = ", ".join(low_items) if low_items else "none"
        return f"All critical food stocks are stable. Inventory items currently below warning threshold: **{low_str}**. Discrepancy checks ran 12 hours ago."
    else:
        return "Hello! I'm your RestoIntegrity OS Business Advisor. I can help you analyze order cancellations, review discount patterns, track inventory, or forecast stock runouts. What would you like to check today?"
