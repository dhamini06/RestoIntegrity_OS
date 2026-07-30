# RestoIntegrity OS

**AI-Powered Smart Restaurant Operations Platform**

Built for **VibeAthon 6.0 (2K26) Hackathon**

> **Team:** VibeGuard · **Lead:** K. Dhamini · dhamini467@gmail.com

---

## User Stories Completed

| Level | User Story | Status |
|-------|-----------|--------|
| **Bronze** | US 1 — Modern intuitive interface for customers & management | ✅ |
| **Silver** | US 2 — Secure authentication (Email OTP + Google OAuth) + Role-based access | ✅ |
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

## Authentication System

Production-grade authentication comparable to ChatGPT, Notion, or Slack:

### Login Options
- **Continue with Google** — Full OAuth 2.0 flow (name, email, avatar, auto-provisioning)
- **Continue with Email** — OTP-based email verification

### Security Architecture
| Layer | Implementation |
|-------|---------------|
| **Password hashing** | bcrypt (12 salt rounds) |
| **OTP security** | Cryptographically secure generation (`secrets.choice`), SHA-256 hashed before storage |
| **OTP expiry** | 5-minute time limit, enforced server-side |
| **Rate limiting** | 5 max verification attempts, 30-second resend cooldown |
| **Session management** | Server-side tokens, 12h absolute expiry, 30min inactivity timeout |
| **Audit logging** | Every auth event recorded: login, logout, OTP generated, OTP verified, session expiry |

### Modules
| Module | File | Purpose |
|--------|------|---------|
| Security | `security.py` | bcrypt hashing, OTP generation/validation, token generation |
| Email Service | `email_service.py` | SMTP email with branded HTML template (Gmail/Resend) |
| OAuth | `oauth.py` | Google OAuth 2.0 flow (auth URL, code exchange, user info) |
| Session Manager | `session_manager.py` | Session CRUD, activity tracking, expiration, cleanup |
| Authentication | `authentication.py` | Orchestration: request OTP, verify OTP, Google login, logout, audit |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (Premium Dark SaaS Theme) |
| **Backend** | Python 3.10+ |
| **Database** | SQLite with WAL mode |
| **AI** | Google Gemini API (`gemini-2.5-flash`) |
| **Charts** | Plotly (Dark Theme) |
| **Auth** | Email OTP (SMTP) + Google OAuth 2.0 |
| **Security** | bcrypt, SHA-256, server-side sessions |
| **Deployment** | Streamlit Community Cloud |
| **Version Control** | GitHub |

---

## Configuration

Create `.streamlit/secrets.toml` with your credentials:

```toml
# Google OAuth
GOOGLE_OAUTH_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET = "your-client-secret"
GOOGLE_OAUTH_REDIRECT_URI = "https://your-app.streamlit.app/"

# SMTP (Gmail or Resend)
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your-email@gmail.com"
SMTP_PASS = "your-app-password"
SMTP_FROM_EMAIL = "your-email@gmail.com"

# Gemini AI (Optional — app works without it)
GEMINI_API_KEY = "your-gemini-api-key"
```

The app works fully without any secrets configured. Email auth falls back gracefully, Google button hides when unconfigured, AI features use offline fallbacks.

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
| dhamini467@gmail.com | Dhamini@123 | **admin** | Full access — all views |
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
