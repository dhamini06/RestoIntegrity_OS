# RestoIntegrity OS 📊

**AI-Powered Smart Restaurant Operations Platform**

Built for **VibeAthon 6.0 (2K26) Hackathon** under **Team VibeGuard**.

> **Team Lead:** K. Dhamini · **Email:** dhamini467@gmail.com
>
> **Phases Completed:** 4 / 5

---

## 🏆 Progress — 4/5 Phases Complete

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1: Foundation** | ✅ Complete | Database schema, user auth, seed data with realistic transactions |
| **Phase 2: Customer Experience** | ✅ Complete | Digital menu, QR ordering, cart with tips, AI upsell recommendations |
| **Phase 3: Kitchen Operations** | ✅ Complete | Live ticket pipeline, stock deduction on completion, void restore |
| **Phase 4: Manager Intelligence** | ✅ Complete | Operations dashboard, revenue analytics, item performance, time patterns, tip tracking, AI Business Advisor, predictive stock forecasting, live operations feed |
| **Phase 5: Deployment & Polish** | 🔄 In Progress | Streamlit Cloud deployment, theme polish, bug fixes |

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
* **📈 Revenue Analytics**: Sales breakdowns by time period, item popularity (best/worst sellers), and staff performance.
* **⏰ Time Pattern Analysis**: Hourly heatmaps, peak hour detection, day-of-week trends to optimize staffing.
* **💰 Tip & Staff Tracking**: Per-waiter tip earnings, average tip percentages, and payment method breakdowns.
* **📋 Live Operations Feed**: Real-time alerts for high cancellation rates, unusual discount patterns, and stock depletion warnings.
* **🔮 Predictive Stock Forecasting**: AI-powered estimates for when ingredients will run out based on sales velocity.
* **🤖 AI Business Advisor**: Natural language chat for querying sales, inventory, and operational patterns.

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit with luxury white & gold theme — Playfair Display serif headings, Inter body font.
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
| Username | Password | Role | Access |
|----------|----------|------|--------|
| admin | admin123 | **admin** | Full access — Manager Dashboard, Customer Menu, Kitchen View |
| alice | alice123 | **staff** | Waiter — Customer Menu, Kitchen View |
| bob | bob123 | **staff** | Waiter — Customer Menu, Kitchen View |
| charlie | charlie123 | **staff** | Waiter — Customer Menu, Kitchen View |
| chef_ramsay | chef123 | **kitchen** | Kitchen View only |
| guest | guest123 | **customer** | Customer Menu only |

---

## 👥 Roles & Permissions

| Role | Access | Description |
|------|--------|-------------|
| **admin** | 📊 Manager Dashboard · 📱 Customer Menu · 👨‍🍳 Kitchen View | Full control. Views all analytics, alerts, AI insights, inventory, staff tips, and time patterns. Can simulate operational scenarios. Can configure Gemini API key. |
| **staff** (waiter) | 📱 Customer Menu · 👨‍🍳 Kitchen View | Can place and manage customer orders. Can view kitchen ticket pipeline to track order status. |
| **kitchen** (chef) | 👨‍🍳 Kitchen View | Sees the live ticket pipeline — pending, preparing, completed orders with aging badges. Can mark orders as preparing/complete. |
| **customer** (guest) | 📱 Customer Menu | Self-service digital menu. Browses items, adds to cart, customizes with tip and payment method, places orders. |

## 🔗 Live Demo

**https://restointegrityos-copcp7vrmntkfjrhabjb9u.streamlit.app/**
