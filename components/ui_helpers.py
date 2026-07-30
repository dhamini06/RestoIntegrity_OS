import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    * {
        font-family: 'Inter', 'Manrope', sans-serif;
    }

    html, body {
        background-color: #09090B !important;
        color: #FAFAFA !important;
    }

    .main, .block-container {
        max-width: 100% !important;
        padding: 1rem 1.5rem !important;
    }

    div[data-testid="stSidebarNavItems"] { padding-top: 0.5rem; }
    div[data-testid="stSidebarNav"]::before { display: none; }

    section[data-testid="stSidebar"] > div:nth-child(1) {
        background: #111113;
        border-right: 1px solid rgba(255,255,255,0.04);
    }
    section[data-testid="stSidebar"] .sidebar-content {
        background: #111113;
    }

    div[data-testid="stMetric"] {
        background: #1F1F23;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 16px;
        padding: 12px 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    div[data-testid="stMetric"] > div:first-child {
        font-size: 0.75rem;
        color: #71717A;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #FAFAFA;
        font-weight: 800;
        font-size: 1.8rem;
    }

    div.stButton > button[kind="primary"] {
        background: #C9A86A !important;
        color: #09090B !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 20px rgba(201,168,106,0.2) !important;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(201,168,106,0.3) !important;
    }
    div.stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #A1A1AA !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        padding: 12px 20px !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: rgba(201,168,106,0.3) !important;
        color: #FAFAFA !important;
        background: rgba(255,255,255,0.03) !important;
    }
    div.stButton > button[kind="secondaryFormSubmit"] {
        background: transparent !important;
        color: #A1A1AA !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
    }

    div.stTextInput > div > input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 14px !important;
        color: #FAFAFA !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
        padding: 12px 16px !important;
        transition: all 0.25s ease !important;
    }
    div.stTextInput > div > input:focus {
        border-color: #C9A86A !important;
        box-shadow: 0 0 0 3px rgba(201,168,106,0.1) !important;
    }
    div.stTextInput > div > input::placeholder {
        color: #52525B !important;
    }

    div.stAlert {
        background: rgba(201,168,106,0.06) !important;
        border: 1px solid rgba(201,168,106,0.15) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        color: #A1A1AA !important;
    }
    div.stAlert.stError {
        background: rgba(239,68,68,0.08) !important;
        border-color: rgba(239,68,68,0.2) !important;
    }
    div.stAlert.stSuccess {
        background: rgba(34,197,94,0.08) !important;
        border-color: rgba(34,197,94,0.2) !important;
    }
    div.stAlert.stWarning {
        background: rgba(245,158,11,0.08) !important;
        border-color: rgba(245,158,11,0.2) !important;
    }

    div.stSpinner {
        border-color: #C9A86A !important;
    }

    .metric-value-gold {
        font-size: 1.8rem;
        font-weight: 800;
        color: #C9A86A;
        letter-spacing: -0.02em;
    }
    .metric-value-green {
        font-size: 1.8rem;
        font-weight: 800;
        color: #22C55E;
        letter-spacing: -0.02em;
    }
    .metric-value-blue {
        font-size: 1.8rem;
        font-weight: 800;
        color: #3B82F6;
        letter-spacing: -0.02em;
    }
    .metric-value-purple {
        font-size: 1.8rem;
        font-weight: 800;
        color: #A855F7;
        letter-spacing: -0.02em;
    }

    .glass-card {
        background: rgba(31,31,35,0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    }
    .glass-card:hover {
        border-color: rgba(201,168,106,0.1);
        box-shadow: 0 12px 48px rgba(0,0,0,0.3);
    }

    .badge-gold {
        background: rgba(201,168,106,0.12);
        color: #C9A86A;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .badge-green {
        background: rgba(34,197,94,0.12);
        color: #22C55E;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .divider {
        height: 1px;
        background: rgba(255,255,255,0.06);
        margin: 16px 0;
    }

    div[data-testid="stExpander"] {
        background: #1F1F23;
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 14px;
        padding: 0;
    }
    div[data-testid="stExpander"] > div[data-testid="stExpanderToggleIcon"] {
        color: #71717A;
    }

    div[data-testid="stRadio"] > div {
        gap: 4px;
    }
    div[data-testid="stRadio"] label {
        background: transparent;
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 12px;
        padding: 8px 16px;
        font-size: 0.82rem;
        font-weight: 500;
        color: #A1A1AA;
        transition: all 0.25s ease;
        cursor: pointer;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(255,255,255,0.04);
        border-color: rgba(201,168,106,0.1);
        color: #FAFAFA;
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        background: rgba(201,168,106,0.1);
        border-color: rgba(201,168,106,0.2);
        color: #C9A86A;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 16px;
        overflow: hidden;
    }

    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4 {
        color: #FAFAFA;
    }

    div[data-testid="column"] {
        gap: 0 !important;
    }

    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes scaleIn {
        0% { opacity: 0; transform: scale(0.95); }
        100% { opacity: 1; transform: scale(1); }
    }
    @keyframes countUp {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)


def inject_auth_css():
    st.markdown("""
    <style>
    /* ── Hide Streamlit chrome during login ──────────────────── */
    /* This CSS is only in the DOM when auth page renders */
    header, footer, #stHeader, .stAppToolbar, .stAppDeployButton,
    div[data-testid="stToolbar"], div[data-testid="stDecoration"],
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .main, .block-container, div[data-testid="stAppViewContainer"],
    div[data-testid="stAppViewBlock"] {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    .stApp > header { display: none !important; }

    /* ── Keyframes ──────────────────────────────────────────── */
    @keyframes authFadeInUp {
        0% { opacity: 0; transform: translateY(24px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes authScaleIn {
        0% { opacity: 0; transform: scale(0.94); }
        100% { opacity: 1; transform: scale(1); }
    }
    @keyframes authFloatSlow {
        0%, 100% { transform: translate(0,0) rotate(0deg); }
        33% { transform: translate(16px,-12px) rotate(1deg); }
        66% { transform: translate(-8px,10px) rotate(-1deg); }
    }
    @keyframes authPulse {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.08); }
    }
    @keyframes authParticle {
        0% { transform: translateY(0) translateX(0) scale(1); opacity: 0; }
        10% { opacity: 0.6; }
        90% { opacity: 0.4; }
        100% { transform: translateY(-600px) translateX(80px) scale(0); opacity: 0; }
    }
    @keyframes authParticle2 {
        0% { transform: translateY(0) translateX(0) scale(1); opacity: 0; }
        10% { opacity: 0.5; }
        90% { opacity: 0.3; }
        100% { transform: translateY(-400px) translateX(-60px) scale(0); opacity: 0; }
    }
    @keyframes authRayMove {
        0% { transform: rotate(-8deg) translateX(-20%); }
        50% { transform: rotate(8deg) translateX(20%); }
        100% { transform: rotate(-8deg) translateX(-20%); }
    }
    @keyframes authGoldShimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes authGlowPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(201,168,106,0.15); }
        50% { box-shadow: 0 0 40px rgba(201,168,106,0.3); }
    }
    @keyframes authBarGrow {
        0% { height: 0%; }
        100% { height: var(--h); }
    }

    /* ── Background ─────────────────────────────────────────── */
    .auth-bg {
        position: fixed;
        inset: 0;
        z-index: 0;
        overflow: hidden;
        background: #09090B;
    }
    .auth-bg-grid {
        position: absolute; inset: 0;
        background-image:
            linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
        background-size: 80px 80px;
    }
    .auth-bg-glow {
        position: absolute;
        width: 700px; height: 700px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(201,168,106,0.07) 0%, transparent 65%);
        top: -250px; right: -100px;
        animation: authFloatSlow 14s ease-in-out infinite;
    }
    .auth-bg-glow-2 {
        position: absolute;
        width: 500px; height: 500px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(59,130,246,0.04) 0%, transparent 65%);
        bottom: -150px; left: -100px;
        animation: authFloatSlow 18s ease-in-out infinite reverse;
    }
    .auth-bg-glow-3 {
        position: absolute;
        width: 400px; height: 400px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(168,85,247,0.03) 0%, transparent 60%);
        top: 40%; left: 30%;
        animation: authFloatSlow 12s ease-in-out infinite 3s;
    }
    .auth-bg-circle {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px);
    }
    .auth-bg-circle-1 {
        width: 350px; height: 350px;
        background: rgba(201,168,106,0.04);
        top: 15%; right: 30%;
        animation: authFloatSlow 20s ease-in-out infinite;
    }
    .auth-bg-circle-2 {
        width: 250px; height: 250px;
        background: rgba(59,130,246,0.03);
        bottom: 20%; right: 10%;
        animation: authFloatSlow 16s ease-in-out infinite reverse;
    }
    .auth-bg-circle-3 {
        width: 200px; height: 200px;
        background: rgba(34,197,94,0.03);
        top: 60%; left: 10%;
        animation: authFloatSlow 22s ease-in-out infinite 5s;
    }
    .auth-bg-ray {
        position: absolute;
        width: 300px; height: 100vh;
        background: linear-gradient(180deg, transparent 0%, rgba(201,168,106,0.02) 50%, transparent 100%);
        transform: rotate(-8deg);
        animation: authRayMove 10s ease-in-out infinite;
    }
    .auth-bg-ray-1 { left: 10%; animation-delay: 0s; }
    .auth-bg-ray-2 { left: 30%; animation-delay: 3s; opacity: 0.5; }
    .auth-bg-ray-3 { left: 50%; animation-delay: 6s; opacity: 0.3; }
    .auth-particle {
        position: absolute;
        width: 3px; height: 3px;
        border-radius: 50%;
        background: #C9A86A;
        opacity: 0;
    }
    .auth-particle:nth-child(1)  { left: 15%; top: 80%; animation: authParticle 8s ease-in-out infinite 0s; }
    .auth-particle:nth-child(2)  { left: 25%; top: 70%; animation: authParticle2 11s ease-in-out infinite 1s; width: 2px; height: 2px; }
    .auth-particle:nth-child(3)  { left: 40%; top: 85%; animation: authParticle 9s ease-in-out infinite 2s; background: #3B82F6; }
    .auth-particle:nth-child(4)  { left: 55%; top: 75%; animation: authParticle2 10s ease-in-out infinite 0.5s; width: 4px; height: 4px; }
    .auth-particle:nth-child(5)  { left: 70%; top: 90%; animation: authParticle 12s ease-in-out infinite 3s; }
    .auth-particle:nth-child(6)  { left: 80%; top: 65%; animation: authParticle2 7s ease-in-out infinite 1.5s; background: #22C55E; width: 2px; height: 2px; }
    .auth-particle:nth-child(7)  { left: 10%; top: 60%; animation: authParticle 13s ease-in-out infinite 4s; background: #A855F7; }
    .auth-particle:nth-child(8)  { left: 60%; top: 50%; animation: authParticle2 9s ease-in-out infinite 2.5s; }
    .auth-particle:nth-child(9)  { left: 35%; top: 40%; animation: authParticle 10s ease-in-out infinite 5s; width: 2px; height: 2px; }
    .auth-particle:nth-child(10) { left: 85%; top: 45%; animation: authParticle2 8s ease-in-out infinite 3.5s; background: #C9A86A; }
    .auth-particle:nth-child(11) { left: 5%;  top: 30%; animation: authParticle 14s ease-in-out infinite 1s; width: 2px; height: 2px; }
    .auth-particle:nth-child(12) { left: 45%; top: 20%; animation: authParticle2 11s ease-in-out infinite 4s; background: #3B82F6; }

    /* ── Hero (left column) ─────────────────────────────────── */
    .auth-hero {
        padding: 48px 64px 48px 16px;
        animation: authFadeInUp 0.6s ease-out;
    }
    .auth-hero-inner {
        display: flex;
        flex-direction: column;
        max-width: 820px;
    }
    .auth-hero-section { opacity: 0; animation: authFadeInUp 0.7s ease-out forwards; }
    .auth-hero-section:nth-child(1) { animation-delay: 0.05s; }
    .auth-hero-section:nth-child(2) { animation-delay: 0.15s; }
    .auth-hero-section:nth-child(3) { animation-delay: 0.25s; }
    .auth-hero-section:nth-child(4) { animation-delay: 0.35s; }
    .auth-hero-section:nth-child(5) { animation-delay: 0.45s; }
    .auth-hero-section:nth-child(6) { animation-delay: 0.55s; }
    .auth-hero-section:nth-child(7) { animation-delay: 0.65s; }

    /* ── Logo ───────────────────────────────────────────────── */
    .auth-logo-row {
        display: flex; align-items: center; gap: 14px; margin-bottom: 12px;
    }
    .auth-logo-icon {
        width: 44px; height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #C9A86A 0%, #B8954E 100%);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 8px 32px rgba(201,168,106,0.2);
        position: relative; overflow: hidden;
    }
    .auth-logo-icon::after {
        content: ''; position: absolute; inset: 0;
        background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.15) 50%, transparent 60%);
        background-size: 200% 200%;
        animation: authGoldShimmer 4s ease-in-out infinite;
    }
    .auth-logo-icon span { color: #09090B; font-weight: 800; font-size: 1.35rem; position: relative; z-index: 1; }
    .auth-logo-text { display: flex; flex-direction: column; }
    .auth-logo-name { font-size: 1rem; font-weight: 700; color: #FAFAFA; letter-spacing: 0.01em; }
    .auth-logo-sub { font-size: 0.72rem; color: #71717A; font-weight: 500; letter-spacing: 0.04em; }

    /* ── Heading ────────────────────────────────────────────── */
    .auth-heading { margin: 32px 0 16px; }
    .auth-heading h1 {
        font-size: clamp(3rem, 4.2vw, 4.5rem);
        font-weight: 800;
        line-height: 1.08;
        letter-spacing: -0.03em;
        margin: 0;
        color: #FAFAFA;
    }
    .auth-heading .gold {
        background: linear-gradient(135deg, #C9A86A 0%, #E8D098 40%, #C9A86A 70%, #B8954E 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: authGoldShimmer 6s linear infinite;
    }
    .auth-desc {
        font-size: clamp(0.9rem, 1.05vw, 1.1rem);
        color: #71717A;
        line-height: 1.65;
        margin: 0 0 40px;
        max-width: 580px;
    }

    /* ── Feature Cards ──────────────────────────────────────── */
    .auth-features {
        display: flex; flex-wrap: wrap; gap: 14px; margin-bottom: 44px;
    }
    .auth-fcard {
        flex: 1 1 140px; min-width: 130px; max-width: 180px;
        background: rgba(24,24,27,0.5);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 18px;
        padding: 18px 16px 16px;
        transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
        cursor: default;
    }
    .auth-fcard:hover {
        background: rgba(30,30,35,0.7);
        border-color: rgba(201,168,106,0.15);
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(0,0,0,0.4), 0 0 40px rgba(201,168,106,0.05);
    }
    .auth-fcard-icon {
        width: 32px; height: 32px; border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 10px; font-size: 0.85rem;
    }
    .auth-fcard-title { font-size: 0.8rem; font-weight: 600; color: #FAFAFA; margin: 0 0 3px; }
    .auth-fcard-desc { font-size: 0.68rem; color: #52525B; margin: 0; line-height: 1.4; }
    .auth-fcard:hover .auth-fcard-desc { color: #71717A; }

    /* ── Dashboard Preview ──────────────────────────────────── */
    .auth-preview {
        background: rgba(18,18,22,0.7);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 22px;
        padding: 22px 24px 24px;
        max-width: 640px;
        margin-bottom: 40px;
        transition: all 0.3s ease;
    }
    .auth-preview:hover {
        border-color: rgba(201,168,106,0.1);
        box-shadow: 0 8px 40px rgba(0,0,0,0.3);
    }
    .auth-preview-top {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 18px;
    }
    .auth-preview-top-left {
        display: flex; align-items: center; gap: 10px;
    }
    .auth-preview-top-left span { font-size: 0.78rem; color: #A1A1AA; font-weight: 500; }
    .auth-preview-live {
        display: inline-flex; align-items: center; gap: 5px;
        font-size: 0.62rem; font-weight: 700; color: #22C55E;
        text-transform: uppercase; letter-spacing: 0.08em;
        padding: 3px 10px; border-radius: 20px;
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.12);
    }
    .auth-preview-live-dot {
        width: 5px; height: 5px; border-radius: 50%;
        background: #22C55E;
        animation: authPulse 2s ease-in-out infinite;
    }
    .auth-preview-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .auth-preview-metric {
        background: rgba(255,255,255,0.02);
        border-radius: 14px; padding: 14px 16px;
        border: 1px solid rgba(255,255,255,0.03);
    }
    .auth-preview-metric-label { font-size: 0.68rem; color: #52525B; font-weight: 500; margin-bottom: 4px; }
    .auth-preview-metric-value { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; color: #FAFAFA; }
    .auth-preview-metric-value.gold { color: #C9A86A; }
    .auth-preview-metric-value.green { color: #22C55E; }
    .auth-preview-metric-value.purple { color: #A855F7; }
    .auth-preview-metric-value.blue { color: #3B82F6; }
    .auth-preview-chart {
        display: flex; align-items: flex-end; gap: 4px;
        height: 36px; margin-top: 8px;
    }
    .auth-preview-chart-bar {
        flex: 1; border-radius: 3px 3px 0 0; min-height: 4px;
        background: linear-gradient(to top, rgba(201,168,106,0.15), rgba(201,168,106,0.35));
        animation: authBarGrow 1s ease-out forwards;
    }
    .auth-preview-chart-bar:nth-child(1) { --h: 55%; height: 55%; }
    .auth-preview-chart-bar:nth-child(2) { --h: 75%; height: 75%; }
    .auth-preview-chart-bar:nth-child(3) { --h: 45%; height: 45%; }
    .auth-preview-chart-bar:nth-child(4) { --h: 90%; height: 90%; }
    .auth-preview-chart-bar:nth-child(5) { --h: 60%; height: 60%; }
    .auth-preview-chart-bar:nth-child(6) { --h: 80%; height: 80%; }
    .auth-preview-chart-bar:nth-child(7) { --h: 70%; height: 70%; }
    .auth-preview-bottom {
        margin-top: 14px; display: flex; justify-content: space-between;
        align-items: center; padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.03);
    }
    .auth-preview-bottom-item { text-align: center; }
    .auth-preview-bottom-item .val { font-size: 0.82rem; font-weight: 700; color: #FAFAFA; }
    .auth-preview-bottom-item .val.gold { color: #C9A86A; }
    .auth-preview-bottom-item .val.green { color: #22C55E; }
    .auth-preview-bottom-item .val.blue { color: #3B82F6; }
    .auth-preview-bottom-item .lbl { font-size: 0.6rem; color: #52525B; font-weight: 500; margin-top: 2px; }

    /* ── Statistics ─────────────────────────────────────────── */
    .auth-stats { display: flex; gap: 28px; flex-wrap: wrap; margin-bottom: 36px; }
    .auth-stat { display: flex; flex-direction: column; }
    .auth-stat-value { font-size: 1.8rem; font-weight: 800; color: #FAFAFA; letter-spacing: -0.02em; line-height: 1; }
    .auth-stat-value.gold { color: #C9A86A; }
    .auth-stat-label { font-size: 0.7rem; color: #52525B; font-weight: 500; margin-top: 3px; }

    /* ── Social Proof ───────────────────────────────────────── */
    .auth-social {
        display: flex; align-items: center; gap: 28px; flex-wrap: wrap; padding-bottom: 8px;
    }
    .auth-social-label { font-size: 0.65rem; color: #3F3F46; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
    .auth-social-name { font-size: 0.8rem; color: #3F3F46; font-weight: 500; letter-spacing: 0.02em; transition: color 0.25s ease; }
    .auth-social-name:hover { color: #71717A; }

    /* ── Auth Card (Right Panel) ────────────────────────────── */
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2),
    div[data-testid="column"]:nth-of-type(2).auth-card-col {
        background: rgba(20,20,24,0.72);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 28px;
        padding: 44px 40px 36px !important;
        box-shadow: 0 32px 96px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.02) inset;
        animation: authScaleIn 0.6s ease-out 0.1s both;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) > div {
        width: 100%;
    }
    .auth-card-logo {
        width: 56px; height: 56px;
        margin: 0 auto 18px;
        position: relative;
        display: flex; align-items: center; justify-content: center;
    }
    .auth-card-logo-hex {
        width: 56px; height: 56px;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        background: linear-gradient(135deg, rgba(201,168,106,0.2) 0%, rgba(201,168,106,0.05) 100%);
        border: 1.5px solid rgba(201,168,106,0.4);
        display: flex; align-items: center; justify-content: center;
        animation: authGlowPulse 3s ease-in-out infinite;
    }
    .auth-card-logo-hex-inner {
        width: 40px; height: 40px;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        background: linear-gradient(135deg, #C9A86A 0%, #B8954E 100%);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 30px rgba(201,168,106,0.2);
    }
    .auth-card-logo-hex-inner span { color: #09090B; font-weight: 800; font-size: 1rem; }
    .auth-card-heading { text-align: center; margin-bottom: 6px; }
    .auth-card-heading h2 { font-size: 1.45rem; font-weight: 700; color: #FAFAFA; margin: 0; letter-spacing: -0.01em; }
    .auth-card-subtitle { text-align: center; font-size: 0.8rem; color: #71717A; margin: 0 0 20px; }
    .auth-card-divider {
        width: 36px; height: 2.5px;
        background: linear-gradient(90deg, #C9A86A, rgba(201,168,106,0.3));
        border-radius: 4px; margin: 0 auto 24px;
    }
    .auth-divider-or {
        display: flex; align-items: center; gap: 16px; margin: 16px 0;
    }
    .auth-divider-or-line {
        flex: 1; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(201,168,106,0.15), transparent);
    }
    .auth-divider-or-text {
        font-size: 0.7rem; color: #52525B; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.06em;
    }
    .auth-google-btn {
        width: 100%;
        padding: 13px 20px; border-radius: 14px;
        font-weight: 600; font-family: inherit;
        font-size: 0.875rem; letter-spacing: 0.01em;
        background: #FAFAFA; color: #09090B; border: none;
        cursor: pointer;
        display: flex; align-items: center; justify-content: center; gap: 10px;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
        box-shadow: 0 4px 24px rgba(255,255,255,0.08);
    }
    .auth-google-btn:hover {
        box-shadow: 0 8px 40px rgba(255,255,255,0.12);
        transform: translateY(-2px);
    }
    .auth-security {
        display: flex; gap: 8px; margin: 22px 0 18px; justify-content: center;
    }
    .auth-security-item {
        flex: 1; text-align: center; padding: 10px 6px; border-radius: 12px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.03);
        transition: all 0.25s ease;
    }
    .auth-security-item:hover {
        background: rgba(255,255,255,0.04);
        border-color: rgba(255,255,255,0.06);
    }
    .auth-security-icon { font-size: 1rem; margin-bottom: 4px; }
    .auth-security-title { font-size: 0.62rem; font-weight: 600; color: #A1A1AA; margin: 0; }
    .auth-security-desc { font-size: 0.55rem; color: #52525B; margin: 1px 0 0; line-height: 1.2; }
    .auth-card-footer { text-align: center; margin-top: 6px; }
    .auth-card-footer p { font-size: 0.68rem; color: #52525B; margin: 0; }
    .auth-card-footer a { color: #C9A86A; text-decoration: none; font-weight: 500; }
    .auth-card-footer a:hover { color: #E8D098; text-decoration: underline; }
    .auth-enterprise { text-align: center; margin-top: 16px; }
    .auth-enterprise span { font-size: 0.62rem; color: #3F3F46; font-weight: 500; letter-spacing: 0.02em; }
    .auth-enterprise-sep { margin: 0 8px; color: #3F3F46; }

    /* ── Auth Flow Pages ────────────────────────────────────── */
    .auth-flow-header { text-align: center; margin-bottom: 20px; }
    .auth-flow-header .icon-wrap {
        width: 44px; height: 44px; border-radius: 14px;
        margin: 0 auto 12px; display: flex; align-items: center; justify-content: center;
    }
    .auth-flow-header h3 { font-size: 1.05rem; font-weight: 700; color: #FAFAFA; margin: 0 0 2px; }
    .auth-flow-header p { font-size: 0.78rem; color: #71717A; margin: 0; }
    .auth-sent-box {
        background: rgba(26,24,16,0.7); border: 1px solid rgba(201,168,106,0.12);
        border-radius: 16px; padding: 18px; text-align: center; margin-bottom: 20px;
    }
    .auth-sent-icon {
        width: 44px; height: 44px; border-radius: 50%;
        background: rgba(201,168,106,0.08);
        display: flex; align-items: center; justify-content: center; margin: 0 auto 8px;
    }
    .auth-sent-icon svg { stroke: #C9A86A; }
    .auth-sent-check { font-size: 0.78rem; color: #22C55E; font-weight: 500; display: inline-flex; align-items: center; gap: 4px; }
    .auth-sent-hint { font-size: 0.68rem; color: #52525B; margin: 4px 0 0; }

    /* ── Responsive ─────────────────────────────────────────── */
    @media (max-width: 1200px) {
        .auth-hero { padding: 40px 40px 40px 16px; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            padding: 36px 32px 32px !important;
        }
        .auth-preview-grid { gap: 12px; }
    }
    @media (max-width: 1024px) {
        .auth-hero { padding: 40px 32px 24px; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            padding: 24px 32px 32px !important;
        }
        .auth-hero-inner { max-width: 100%; }
        .auth-heading h1 { font-size: clamp(2.2rem, 6vw, 3.2rem); }
        .auth-features { gap: 10px; }
        .auth-fcard { flex: 1 1 120px; min-width: 110px; max-width: none; padding: 14px 12px; }
        .auth-preview { max-width: 100%; }
        .auth-stats { gap: 20px; }
        .auth-stat-value { font-size: 1.4rem; }
    }
    @media (max-width: 640px) {
        .auth-hero { padding: 28px 20px 16px; }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
            padding: 28px 22px 24px !important;
            border-radius: 22px;
        }
        .auth-logo-icon { width: 36px; height: 36px; }
        .auth-logo-icon span { font-size: 1.1rem; }
        .auth-heading { margin: 20px 0 12px; }
        .auth-heading h1 { font-size: clamp(1.8rem, 8vw, 2.4rem); }
        .auth-desc { margin-bottom: 24px; font-size: 0.85rem; }
        .auth-features { gap: 8px; }
        .auth-fcard { flex: 1 1 calc(50% - 8px); min-width: 0; max-width: none; padding: 12px 10px; }
        .auth-fcard-icon { width: 28px; height: 28px; font-size: 0.75rem; }
        .auth-fcard-title { font-size: 0.72rem; }
        .auth-preview { padding: 16px; margin-bottom: 24px; }
        .auth-preview-grid { grid-template-columns: 1fr; gap: 10px; }
        .auth-stats { gap: 16px; justify-content: space-between; }
        .auth-stat-value { font-size: 1.2rem; }
        .auth-social { gap: 16px; }
        .auth-social-name { font-size: 0.72rem; }
        .auth-security { flex-direction: column; gap: 6px; }
        .auth-card-heading h2 { font-size: 1.2rem; }
        .auth-preview-bottom { flex-wrap: wrap; gap: 10px; }
    }
    </style>
    """, unsafe_allow_html=True)


def show_glass_card(title, content_html, icon="", color="gold"):
    st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                <span style="font-size:1.2rem;">{icon}</span>
                <h4 style="margin:0; font-size:1rem; color:#FAFAFA;">{title}</h4>
            </div>
            <div>
                {content_html}
            </div>
        </div>
    """, unsafe_allow_html=True)


def show_metric_card(label, value, icon="", color="gold"):
    val_class = f"metric-value-gold" if color == "gold" else f"metric-value-{color}"
    st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:20px;">
            <div style="font-size:1.5rem; margin-bottom:4px;">{icon}</div>
            <div style="font-size:0.75rem; color:#71717A; font-weight:500; text-transform:uppercase; letter-spacing:0.06em;">{label}</div>
            <div class="{val_class}">{value}</div>
        </div>
    """, unsafe_allow_html=True)
