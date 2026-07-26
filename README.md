# RestoIntegrity OS 📊

**AI-Powered Smart Restaurant Operations Platform**

Built for **VibeAthon 6.0 (2K26) Hackathon** under **Team VibeGuard**.

RestoIntegrity OS is a modern restaurant management platform that gives owners real-time visibility into what's actually happening in their business — sales performance, inventory health, staff tip tracking, and AI-powered operational insights. Run smarter, waste less, earn more.

---

## 🌟 Why This Exists

Restaurants run on razor-thin margins (typically 3-5%). The difference between profitability and failure comes down to operational visibility — knowing which items sell, managing inventory before you run out, understanding staff performance, and catching small problems before they become expensive ones.

Most restaurant POS systems show you what happened yesterday. RestoIntegrity OS shows you what's happening right now and what to do about it.

---

## 🚀 Key Features

### Customer Experience
* **📱 Digital Menu with Live Stock**: QR-based ordering with real-time availability. Customers see what's in stock and order directly from their table.
* **🧠 AI Pairing Recommendations**: Smart upselling that suggests complementary items based on what's already in the cart.

### Kitchen Operations
* **👨‍🍳 Live Ticket Pipeline**: Order flow from Pending → Preparing → Completed with timestamp tracking and aging badges.
* **📦 Inventory Integration**: Stock levels auto-deduct on order completion. Voided orders restore inventory automatically.

### Manager Intelligence
* **📊 Operations Command Center**: Single dashboard with revenue metrics, order trends, cancellation rates, and inventory health.
* **📈 Revenue Analytics**: Sales breakdowns by time period, item popularity, and staff performance.
* **💰 Tip & Staff Tracking**: Per-waiter tip earnings, average tip percentages, and payment method breakdowns.
* **📋 Live Operations Feed**: Real-time alerts for high cancellation rates, unusual discount patterns, and stock depletion warnings.
* **🔮 Predictive Stock Forecasting**: AI-powered estimates for when ingredients will run out based on sales velocity.
* **🤖 AI Business Advisor**: Natural language chat for querying sales, inventory, and operational patterns.

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit with custom CSS — bright gradient theme, Poppins font, glassmorphism panels.
* **Database**: SQLite — zero-config, pre-populated with realistic multi-day transaction data.
* **AI Engine**: Google Gemini API (`gemini-2.5-flash`) for operational insights, stock forecasting, and smart recommendations.
* **Hosting**: Streamlit Community Cloud (free, instant GitHub sync).

---

## 🤖 AI Usage

Gemini powers three operational intelligence features:
1. **Alert Analysis**: Automatically classifies and prioritizes operational events with recommended actions.
2. **Stock Forecasting**: Predicts ingredient runout timelines based on sales velocity.
3. **Business Advisor**: Context-aware chat assistant for real-time operational queries.

*The app includes robust offline fallbacks and works fully without an API key.*

---

## 💻 Local Setup

### Prerequisites
- Python 3.10+

### Quick Start
```bash
git clone <your-repository-url>
cd resto-integrity-os
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### Demo Credentials
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Manager |
| alice | alice123 | Server |
| bob | bob123 | Server |
| charlie | charlie123 | Server |
| chef_ramsay | chef123 | Kitchen |
| guest | guest123 | Customer |

---

## 🔗 Live Demo
*[Enter hosted URL after deployment]*
