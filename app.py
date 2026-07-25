import streamlit as st
import os
from components.ui_helpers import inject_custom_css
from components.customer_view import render_customer_view
from components.kitchen_view import render_kitchen_view
from components.manager_view import render_manager_view

# Configure page metadata
st.set_page_config(
    page_title="RestoIntegrity OS - Operational Security OS",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom glassmorphism styling
inject_custom_css()

# Main app title banner
st.markdown("""
<div style="background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); padding: 15px; border-radius: 12px; margin-bottom: 25px;">
    <h1 style="color: white; margin: 0; font-size: 2.2rem; font-weight: 800; text-align: center;">
        🛡️ RestoIntegrity OS
    </h1>
    <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 1rem; font-weight: 500; text-align: center;">
        Smart Restaurant Platform with built-in Operational Integrity & Loss Prevention Guardrails
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation Panel
st.sidebar.markdown("<h2 class='glow-text-cyan'>🧭 Role Simulation</h2>", unsafe_allow_html=True)
st.sidebar.write("Switch roles to experience different layers of the operational workflow:")

role = st.sidebar.radio(
    "Choose Active Session:",
    ["📱 Customer (Order Menu)", "👨‍🍳 Kitchen (Ticket Feed)", "🛡️ Manager (Security & Analytics)"],
    index=2 # Default to Manager to showcase the main dashboard first
)

st.sidebar.markdown("---")

# Settings Panel for API Keys
st.sidebar.markdown("<h3 class='glow-text-amber'>⚙️ AI Integration Settings</h3>", unsafe_allow_html=True)
st.sidebar.write("Optionally run live Gemini investigations by providing your Google AI Studio key:")

api_key = st.sidebar.text_input("Google Gemini API Key:", type="password", value=os.getenv("GEMINI_API_KEY", ""))
if api_key:
    os.environ["GEMINI_API_KEY"] = api_key
    st.sidebar.success("🔑 Key active! Live AI models enabled.")
else:
    # If no key, remove key from env if it was set
    if "GEMINI_API_KEY" in os.environ:
        del os.environ["GEMINI_API_KEY"]
    st.sidebar.warning("⚠️ Running in offline fallback mode. AI simulations will use static templates.")

st.sidebar.markdown("---")

# Quick Pitch Info Box
st.sidebar.markdown("<h3 class='glow-text-purple'>💡 The Winning Hack</h3>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="background: rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; font-size: 0.85rem; line-height: 1.4;">
    <strong>Operational Integrity Layer:</strong><br>
    Most restaurant systems focus on Guest convenience. 
    RestoIntegrity OS addresses <strong>loss prevention</strong> (fraud, cash skimming, inventory shrinkage) 
    using cybersecurity anomaly principles, making it a highly innovative SaaS.
</div>
""", unsafe_allow_html=True)

# Route views based on active role
if role == "📱 Customer (Order Menu)":
    render_customer_view()
elif role == "👨‍🍳 Kitchen (Ticket Feed)":
    render_kitchen_view()
else:
    render_manager_view()
