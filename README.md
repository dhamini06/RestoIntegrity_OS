# RestoIntegrity OS 🛡️

**A Smart Restaurant Management Platform with an Operational Integrity & Loss Prevention Layer.**

Built for **VibeAthon 6.0 (2K26) Hackathon** under **Team VibeGuard**.

RestoIntegrity OS is a modern restaurant system that goes beyond guest convenience (QR menus, online ordering) to solve the most critical, invisible problem in restaurant operations: **internal transaction fraud, discount leaks, and inventory shrinkage (slippage).**

---

## 🌟 Pitch Context & Concept

Restaurants operate on razor-thin profit margins (typically 3-5%) and lose up to **10% of gross revenue** to minor inefficiencies and internal leakages:
1. **Cash Skimming**: Staff pocketing cash from customers, serving food, and then "voiding" the transaction in the POS afterward to hide the cash trail.
2. **Discount Abuse**: Manual, high-percentage discounts applied without supervisor logging.
3. **Inventory Shrinkage**: Discrepancies between theoretical usage (calculated from sales counts) and physical kitchen stock levels due to unlogged waste or theft.

**Our Hack:** We treat restaurant transaction and inventory flows like a cybersecurity SIEM system. The application hosts a guest QR ordering interface, a kitchen ticket pipeline, and a **manager Security Dashboard (SOC)** with real-time anomaly detection rules, visual sales analytics, and a **Gemini AI Forensic Investigator**.

---

## 🚀 Key Features & User Stories Completed

### Bronze & Silver Level (User Experience & Ordering)
* **📱 Live Availability Guest Menu**: Seamless digital menu where customers scan Table QRs, check live stock limits, and place orders. Stock limits count down in real-time.
* **👨‍🍳 Kitchen Ticket Pipeline**: Fulfill order flows (Pending -> Preparing -> Completed/Served) with chronological wait time counters.

### Gold Level (Operations & Inventory Management)
* **📊 Visual Sales Analytics**: Dynamic hourly sales charts (Plotly) displaying verified gross revenue and order frequencies.
* **🥦 Real-time Inventory Reconciliation**: Tools for managers to input physical stock levels, automatically comparing them to theoretical levels.

### Platinum & Bonus Level (Intelligent Operations)
* **🚨 Real-Time Security Logs (SOC Feed)**: Active alert banners for high-risk behaviors:
  - Voids applied to orders *after* preparation started (Skimming danger).
  - Manual discounts exceeding 30%.
  - Physical counts indicating high inventory leakage.
* **🧠 Gemini AI Incident Forensics**: Automatically investigates triggered alerts to provide threat classification, risk ratings, and next-step actions.
* **🔮 Predictive Demand Forecasting**: Gemini-powered stock runout estimation.
* **💬 Manager AI Co-Pilot Assistant**: Natural language chat interface allowing managers to query security logs, inventory status, and sales metrics ("Audit Bob's void alert", "What items are critical?").
* **✨ Customer Pairing Recommendations**: AI-powered upselling cart widget.

---

## 🛠️ Tech Stack & Architecture

* **Frontend & UI**: Streamlit (Python) - styled with custom CSS variables, dark-mode, and glassmorphic panels for a premium SaaS experience.
* **Database**: SQLite - zero cost, single-file relational database pre-populated with 48 hours of high-fidelity transaction data.
* **AI Engine**: Google Gemini API (`gemini-2.5-flash` via the `google-genai` Python SDK).
* **Version Control**: Git & GitHub.
* **Hosting**: Streamlit Community Cloud (100% Free, instant sync to GitHub).

---

## 🤖 AI Usage

This application leverages Gemini AI in three key areas:
1. **Loss Prevention Audits**: Generates detailed forensic summaries of logged POS anomalies.
2. **Stock Forecasting**: Analyzes ingredient depletion velocities.
3. **Interactive Support**: Empowers managers with a context-aware chat assistant querying live SQL data.

*Note: The app contains robust local rule-based fallbacks to remain fully interactive even if no API key is set.*

---

## 💻 Local Setup Instructions

### Prerequisites
- Python 3.10+ installed.

### Setup
1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd resto-integrity-os
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```
4. Access the app in your browser at `http://localhost:8501`.

---

## 🔗 Hosted Demo Link
- **Live Link**: *[Enter Hosted URL here after deployment]*
