# RestoIntegrity OS

**AI-Powered Smart Restaurant Operations Platform**

Built for **VibeAthon 6.0 (2K26) Hackathon**

> **Team:** VibeGuard · **Lead:** K. Dhamini · dhamini467@gmail.com

---

## User Stories Completed

| Level | User Story | Status |
|-------|-----------|--------|
| **Bronze** | US 1 — Modern intuitive interface for customers & management | ✅ |
| **Silver** | US 2 — Secure authentication (Email OTP + Google OAuth) + Role-based access | ⏳ **Pending** |
| **Silver** | US 3 — Digitized workflows: Digital Menu, Live Availability, Smart Reservations, Order Management, Queue Management, Billing, Notifications | ✅ |
| **Gold** | US 4 — Management Dashboard: Orders, Tables, Inventory, Staff, Customers, Sales, Analytics | ✅ |
| **Platinum** | US 5 — Intelligent features: Personalized Recommendations, Inventory Prediction, Demand Forecasting, Smart Notifications, Operational Insights, AI Assistant | ✅ |
| **Bonus** | Queue/Waitlist Management, Table Management System, In-App Notification Center, Customer History, Live Operations Feed with AI Analysis | ✅ |
| **Bonus** | Executive Dashboard with Restaurant Health Score, Kitchen Bottleneck Detection, AI Copilot | ✅ |
| **Bonus** | Presentation Mode: One-click Demo Population, Lunch Rush Simulation, Data Reset | ✅ |

---

## Key Features

### Customer Experience
- **Digital Menu with Live Stock** — Real-time availability, stock badges, smart pairing recommendations
- **Smart Reservations** — Book tables by date, time, party size; view table availability
- **Queue Management** — Join waitlist, track position, estimated wait times
- **Seamless Checkout** — Cart management, tip selection, payment method, digital receipt
- **Customer Notifications** — Order confirmations, reservation updates

### Kitchen Operations
- **Live Ticket Pipeline** — Pending → Preparing → Completed with aging badges and timestamps
- **Stock Integration** — Auto-deduct on completion, restore on void
- **Order Aging Alerts** — Color-coded badges (Fresh/Aging/STALE/SLOW)
- **Kitchen Bottleneck Detection** — Real-time analysis of cook times, stalled orders, and kitchen load

### Manager Dashboard
- **Executive Dashboard** — Restaurant Health Score (composite of alerts, stock, queue, kitchen load), KPI grid, bottleneck cards, AI-generated smart notifications
- **Operations Hub** — Table management, customer history, anomaly alerts, scenario simulator
- **Revenue Analytics** — Sales by hour, item performance, staff cancellation rates, discount patterns
- **Time Pattern Analysis** — Hourly/daily/weekly heatmaps, peak hour detection
- **Smart Inventory Management** — Stock levels, data-driven consumption forecast with charts, physical count reconciliation
- **Tips & Staff Tracking** — Per-waiter earnings, average tips, tip trends over time
- **AI Restaurant Copilot** — Natural language database query engine with data tables and charts

### Intelligent Operations
- **AI Alert Analysis** — Auto-classifies operational events with risk scoring and recommended actions
- **Smart Stock Forecasting** — Data-driven predictions using actual 30-day sales velocity
- **AI Restaurant Copilot** — Ask anything about revenue, inventory, orders, tips, menu performance, or reservations
- **Kitchen Bottleneck Detection** — Analyzes cook times, stalled orders, and load averages
- **AI Smart Notifications** — Context-aware notifications generated from live data patterns
- **Menu Pairing** — Gemini-powered smart upsell recommendations
- **In-App Notifications** — Real-time alerts for orders, reservations, queue events

### Presentation Mode
- **Populate Demo Data** — One-click generation of 15+ orders, alerts, and inventory
- **Simulate Lunch Rush** — Generate rush orders, reduce inventory, trigger anomalies, fire system notifications
- **Generate Sample Report** — Pre-built AI analysis for judging demos
- **Reset & Fresh Start** — Clean database rebuild

---

## Access

Authentication has been removed for evaluation. The app loads directly as an **admin** user with full access to all views.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (Premium Dark SaaS Theme) |
| **Backend** | Python 3.10+ |
| **Database** | SQLite with WAL mode |
| **AI** | Google Gemini API (`gemini-2.5-flash`) |
| **Charts** | Plotly (Dark Theme) |
| **Access** | Role-based (pre-seeded demo accounts, no login required) |
| **Deployment** | Streamlit Community Cloud |
| **Version Control** | GitHub |

---

## Configuration

The only optional config is the Gemini API key for AI features (the app works fully without it):

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
```

---

## AI Usage

Gemini powers five intelligence features:

1. **Alert Analysis** — Classifies security/operational events with risk scores and recommended actions
2. **Stock Forecasting** — Predicts ingredient runout timelines based on historical sales velocity
3. **Business Advisor** — Context-aware chat assistant for real-time operational queries
4. **Menu Recommendations** — Smart pairing suggestions based on cart contents
5. **AI Copilot** — Natural language database query engine with structured data responses

*The app includes offline fallbacks and works fully without an API key.*

---

## Quick Start

```bash
git clone https://github.com/dhamini06/RestoIntegrity_OS.git
cd RestoIntegrity_OS
pip install -r requirements.txt
streamlit run app.py
```

### Demo Credentials

| Email | Password | Role | Access |
|-------|----------|------|--------|
| admin@resto.com | admin123 | **admin** | Full access — all views |
| alice@resto.com | alice123 | **staff** | Waiter — Reservations, Queue, Customer Menu, Kitchen View |
| bob@resto.com | bob123 | **staff** | Waiter — Reservations, Queue, Customer Menu, Kitchen View |
| charlie@resto.com | charlie123 | **staff** | Waiter — Reservations, Queue, Customer Menu, Kitchen View |
| chef@resto.com | chef123 | **kitchen** | Kitchen View only |
| guest@resto.com | guest123 | **customer** | Customer Menu, Reservations, Queue |

### Roles & Permissions

| Role | Navigation Access |
|------|------------------|
| **admin** | Manager Dashboard · Reservations · Queue · Customer Menu · Kitchen View |
| **staff** | Reservations · Queue · Customer Menu · Kitchen View |
| **kitchen** | Kitchen View |
| **customer** | Customer Menu · Reservations · Queue |

---

## Live Demo

**https://restointegrityos-copcp7vrmntkfjrhabjb9u.streamlit.app/**

---

## Submission Requirements

- [x] Hosted application live and publicly accessible
- [x] GitHub repository public with meaningful commits
- [x] README with team name, tech stack, user stories, AI usage, hosted link
