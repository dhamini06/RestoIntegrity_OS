# RestoIntegrity OS

**AI-Powered Smart Restaurant Operations Platform**

Built for **VibeAthon 6.0 (2K26) Hackathon**

> **Team:** VibeGuard · **Lead:** K. Dhamini · dhamini467@gmail.com

---

## User Stories Completed

| Level | User Story | Status |
|-------|-----------|--------|
| **Bronze** | US 1 — Modern intuitive interface for customers & management | ✅ |
| **Silver** | US 2 — Secure authentication (Email/Password + Google OAuth) + Role-based access | ✅ |
| **Silver** | US 3 — Digitized workflows: Digital Menu, Live Availability, Smart Reservations, Order Management, Queue Management, Billing, Notifications | ✅ |
| **Gold** | US 4 — Management Dashboard: Orders, Tables, Inventory, Staff, Customers, Sales, Analytics | ✅ |
| **Platinum** | US 5 — Intelligent features: Personalized Recommendations, Inventory Prediction, Demand Forecasting, Smart Notifications, Operational Insights, AI Assistant | ✅ |
| **Bonus** | Queue/Waitlist Management, Table Management System, In-App Notification Center, Customer History, Live Operations Feed with AI Analysis | ✅ |

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

### Manager Dashboard
- **Operations Hub** — Table management, customer history, anomaly alerts, scenario simulator
- **Revenue Analytics** — Sales by hour, item performance, staff cancellation rates, discount patterns
- **Time Pattern Analysis** — Hourly/daily/weekly heatmaps, peak hour detection
- **Inventory Management** — Stock levels, AI runout forecast, physical count reconciliation
- **Tips & Staff Tracking** — Per-waiter earnings, average tips, tip trends over time
- **AI Business Advisor** — Natural language chat for operational queries

### Intelligent Operations
- **AI Alert Analysis** — Auto-classifies operational events with risk scoring and recommended actions
- **Stock Forecasting** — ML predictions for ingredient depletion timelines
- **Menu Pairing** — Gemini-powered smart upsell recommendations
- **In-App Notifications** — Real-time alerts for orders, reservations, queue events

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (Premium Dark SaaS Theme) |
| **Backend** | Python 3.10+ |
| **Database** | SQLite |
| **AI** | Google Gemini API (`gemini-2.5-flash`) |
| **Charts** | Plotly (Dark Theme) |
| **Auth** | Email/Password + Google OAuth flow |
| **Deployment** | Streamlit Community Cloud |
| **Version Control** | GitHub |

---

## AI Usage

Gemini powers four intelligence features:
1. **Alert Analysis** — Classifies security/operational events with risk scores and recommended actions
2. **Stock Forecasting** — Predicts ingredient runout timelines based on historical sales velocity
3. **Business Advisor** — Context-aware chat assistant for real-time operational queries
4. **Menu Recommendations** — Smart pairing suggestions based on cart contents

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

| Username | Password | Role | Access |
|----------|----------|------|--------|
| admin | admin123 | **admin** | Full access — Manager Dashboard, Reservations, Queue, Customer Menu, Kitchen View |
| alice | alice123 | **staff** | Waiter — Reservations, Queue, Customer Menu, Kitchen View |
| bob | bob123 | **staff** | Waiter — Reservations, Queue, Customer Menu, Kitchen View |
| charlie | charlie123 | **staff** | Waiter — Reservations, Queue, Customer Menu, Kitchen View |
| chef_ramsay | chef123 | **kitchen** | Kitchen View only |
| guest | guest123 | **customer** | Customer Menu, Reservations, Queue |

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
