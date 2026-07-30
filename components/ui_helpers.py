import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Manrope', sans-serif !important;
            background: #09090B !important;
            color: #FAFAFA !important;
            letter-spacing: 0.01em;
        }

        .main .block-container {
            padding: 1.5rem 2rem !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
        }

        [data-testid="stSidebar"] {
            background: #111113 !important;
            border-right: 1px solid rgba(255,255,255,0.06) !important;
            min-width: 240px !important;
        }
        [data-testid="stSidebar"] .block-container {
            padding: 1.5rem 1rem !important;
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.06) !important;
            margin: 16px 0 !important;
        }

        [data-testid="stHeader"] { display: none !important; }
        div[data-testid="stToolbar"] { display: none !important; }
        footer { display: none !important; visibility: hidden !important; }
        #MainMenu { display: none !important; visibility: hidden !important; }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #09090B; }
        ::-webkit-scrollbar-thumb { background: #27272A; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #3F3F46; }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Manrope', sans-serif !important;
            font-weight: 700 !important;
            color: #FAFAFA !important;
            letter-spacing: 0.02em !important;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes scaleIn {
            from { opacity: 0; transform: scale(0.96); }
            to { opacity: 1; transform: scale(1); }
        }

        .glass-card {
            background: #18181B;
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.5s ease-out;
        }
        .glass-card:hover {
            border-color: rgba(201, 168, 106, 0.15);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
            transform: translateY(-2px);
        }

        .glass-card-subtle {
            background: #1F1F23;
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 18px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        .glass-card-subtle:hover {
            border-color: rgba(255,255,255,0.08);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }

        button {
            border-radius: 14px !important;
            font-weight: 600 !important;
            font-family: 'Manrope', sans-serif !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: none !important;
            letter-spacing: 0.01em !important;
            font-size: 0.875rem !important;
        }
        button:active {
            transform: scale(0.97) !important;
        }

        button[kind="primary"] {
            background: #C9A86A !important;
            color: #09090B !important;
            box-shadow: 0 4px 20px rgba(201, 168, 106, 0.2) !important;
            padding: 10px 24px !important;
        }
        button[kind="primary"]:hover {
            background: #D4B47A !important;
            box-shadow: 0 6px 24px rgba(201, 168, 106, 0.3) !important;
            transform: translateY(-1px) scale(1.01) !important;
        }

        button[kind="secondary"] {
            background: transparent !important;
            color: #A1A1AA !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
        }
        button[kind="secondary"]:hover {
            background: rgba(255,255,255,0.04) !important;
            border-color: rgba(201, 168, 106, 0.3) !important;
            color: #FAFAFA !important;
        }

        div[data-testid="stExpander"] {
            background: #18181B !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 18px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2) !important;
            margin-bottom: 12px !important;
        }
        div[data-testid="stExpander"] summary {
            font-family: 'Manrope', sans-serif !important;
            font-weight: 600 !important;
            color: #FAFAFA !important;
            font-size: 0.9rem !important;
        }
        div[data-testid="stExpander"] summary:hover {
            color: #C9A86A !important;
        }

        .metric-value {
            font-family: 'Manrope', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 4px 0;
            color: #FAFAFA;
            letter-spacing: -0.02em;
        }
        .metric-value-gold {
            font-family: 'Manrope', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 4px 0;
            color: #C9A86A;
            letter-spacing: -0.02em;
        }
        .metric-value-emerald {
            font-family: 'Manrope', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 4px 0;
            color: #22C55E;
            letter-spacing: -0.02em;
        }
        .metric-value-amber {
            font-family: 'Manrope', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 4px 0;
            color: #F59E0B;
            letter-spacing: -0.02em;
        }
        .metric-value-blue {
            font-family: 'Manrope', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            margin: 4px 0;
            color: #3B82F6;
            letter-spacing: -0.02em;
        }

        .alert-card-high {
            border-left: 3px solid #EF4444;
            background: #1A1111;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid rgba(239,68,68,0.1);
            animation: slideInLeft 0.4s ease-out;
            transition: all 0.3s ease;
        }
        .alert-card-high:hover {
            background: #1F1212;
            border-color: rgba(239,68,68,0.2);
        }
        .alert-card-medium {
            border-left: 3px solid #F59E0B;
            background: #1A1810;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid rgba(245,158,11,0.1);
            animation: slideInLeft 0.4s ease-out;
            transition: all 0.3s ease;
        }
        .alert-card-medium:hover {
            background: #1F1A10;
            border-color: rgba(245,158,11,0.2);
        }
        .alert-card-low {
            border-left: 3px solid #22C55E;
            background: #111A11;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            border: 1px solid rgba(34,197,94,0.1);
            animation: slideInLeft 0.4s ease-out;
        }

        input[type="text"], input[type="password"], input[type="number"], input[type="email"],
        div[data-baseweb="select"], textarea, div[data-baseweb="input"] input {
            background: #1F1F23 !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 14px !important;
            color: #FAFAFA !important;
            font-family: 'Manrope', sans-serif !important;
            font-size: 0.875rem !important;
            padding: 12px 16px !important;
            transition: all 0.2s ease !important;
        }
        input[type="text"]:focus, input[type="password"]:focus, input[type="number"]:focus,
        input[type="email"]:focus, div[data-baseweb="select"]:focus, textarea:focus {
            border-color: #C9A86A !important;
            box-shadow: 0 0 0 3px rgba(201, 168, 106, 0.1) !important;
        }

        label, .stTextInput label, .stSelectbox label {
            color: #A1A1AA !important;
            font-family: 'Manrope', sans-serif !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
        }

        div[role="radiogroup"] {
            display: flex !important;
            flex-direction: column !important;
            gap: 8px !important;
            margin-top: 12px !important;
        }
        div[role="radiogroup"] label {
            background: #18181B !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 14px !important;
            padding: 12px 16px !important;
            color: #A1A1AA !important;
            cursor: pointer !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-family: 'Manrope', sans-serif !important;
            font-weight: 500 !important;
        }
        div[role="radiogroup"] label:hover {
            background: #1F1F23 !important;
            border-color: rgba(201, 168, 106, 0.2) !important;
            color: #FAFAFA !important;
        }
        div[role="radiogroup"] label:has(input[type="radio"]:checked) {
            background: rgba(201, 168, 106, 0.06) !important;
            border-color: #C9A86A !important;
            color: #C9A86A !important;
            box-shadow: 0 0 20px rgba(201, 168, 106, 0.08) !important;
            font-weight: 600 !important;
        }
        div[role="radiogroup"] label input[type="radio"] { display: none !important; }
        div[role="radiogroup"] label div[class*="st-"] { display: none !important; }
        div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
            margin-left: 0 !important; padding: 0 !important;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-family: 'Manrope', sans-serif;
        }
        .badge-critical {
            background: rgba(239,68,68,0.1);
            color: #EF4444;
            border: 1px solid rgba(239,68,68,0.2);
        }
        .badge-medium {
            background: rgba(245,158,11,0.1);
            color: #F59E0B;
            border: 1px solid rgba(245,158,11,0.2);
        }
        .badge-low {
            background: rgba(34,197,94,0.1);
            color: #22C55E;
            border: 1px solid rgba(34,197,94,0.2);
        }
        .badge-gold {
            background: rgba(201,168,106,0.1);
            color: #C9A86A;
            border: 1px solid rgba(201,168,106,0.2);
        }
        .badge-blue {
            background: rgba(59,130,246,0.1);
            color: #3B82F6;
            border: 1px solid rgba(59,130,246,0.2);
        }

        div[data-testid="stTabs"] {
            margin-bottom: 24px;
        }
        div[data-testid="stTabs"] button {
            font-family: 'Manrope', sans-serif !important;
            font-weight: 500 !important;
            font-size: 0.8rem !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
            color: #71717A !important;
            border: 1px solid transparent !important;
            transition: all 0.2s ease !important;
            letter-spacing: 0.01em !important;
        }
        div[data-testid="stTabs"] button:hover {
            color: #A1A1AA !important;
            border-color: rgba(255,255,255,0.06) !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            background: rgba(201, 168, 106, 0.1) !important;
            color: #C9A86A !important;
            border-color: rgba(201, 168, 106, 0.2) !important;
            font-weight: 600 !important;
        }

        .stale-badge {
            background: rgba(239,68,68,0.1) !important;
            color: #EF4444 !important;
            border: 1px solid rgba(239,68,68,0.2) !important;
            font-weight: 700 !important;
            animation: pulseGlow 2s infinite;
        }

        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 8px rgba(239,68,68,0.1); }
            50% { box-shadow: 0 0 16px rgba(239,68,68,0.2); }
        }

        div.stDateInput > div {
            background: #1F1F23 !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 14px !important;
        }
        div.stDateInput > div:focus-within {
            border-color: #C9A86A !important;
            box-shadow: 0 0 0 3px rgba(201, 168, 106, 0.1) !important;
        }
        div.stDateInput input {
            color: #FAFAFA !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 18px !important;
            overflow: hidden !important;
        }

        section[data-testid="stSidebar"] hr {
            margin: 16px 0 !important;
        }

        .gold-text {
            color: #C9A86A;
        }

        .divider {
            height: 1px;
            background: rgba(255,255,255,0.06);
            margin: 24px 0;
        }

        .stAlert {
            background: #1F1F23 !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 14px !important;
            color: #FAFAFA !important;
        }
        .stAlert > div:first-child {
            color: #C9A86A !important;
        }

        div.stSelectbox div[data-baseweb="select"] {
            background: #1F1F23 !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 14px !important;
        }
        div.stSelectbox div[data-baseweb="select"]:hover {
            border-color: rgba(201, 168, 106, 0.3) !important;
        }
        div.stSelectbox ul {
            background: #18181B !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 14px !important;
        }
        div.stSelectbox li {
            color: #A1A1AA !important;
        }
        div.stSelectbox li:hover {
            background: rgba(201, 168, 106, 0.08) !important;
            color: #FAFAFA !important;
        }

        div.stSlider div[data-baseweb="slider"] div {
            background: rgba(255,255,255,0.08) !important;
        }
        div.stSlider div[data-baseweb="slider"] div[role="slider"] {
            background: #C9A86A !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(201, 168, 106, 0.3) !important;
        }

        section.main > div:first-child {
            animation: fadeIn 0.4s ease-out;
        }
        </style>
    """, unsafe_allow_html=True)

def inject_auth_css():
    st.markdown("""
    <style>
    /* ── Base & Keyframes ─────────────────────────────────── */
    @keyframes authFadeInUp {
        0% { opacity: 0; transform: translateY(24px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes authFadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    @keyframes authScaleIn {
        0% { opacity: 0; transform: scale(0.94); }
        100% { opacity: 1; transform: scale(1); }
    }
    @keyframes authFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
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
    @keyframes authBreath {
        0%, 100% { opacity: 0.15; }
        50% { opacity: 0.35; }
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
    @keyframes authSlideUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes authCountIn {
        0% { opacity: 0; transform: translateY(12px); }
        100% { opacity: 1; transform: translateY(0); }
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

    /* ── Split Container ──────────────────────────────────── */
    .auth-split {
        display: flex;
        min-height: 100vh;
        width: 100%;
        position: fixed;
        top: 0; left: 0;
        z-index: 1;
        background: transparent;
    }

    /* ── Background System ─────────────────────────────────── */
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

    /* ── Left Hero (60%) ───────────────────────────────────── */
    .auth-hero {
        flex: 0 0 60%;
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 48px 64px 48px 80px;
        overflow-y: auto;
        background: transparent;
    }
    .auth-hero-inner {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        max-width: 820px;
    }
    .auth-hero-section {
        animation: authFadeInUp 0.7s ease-out forwards;
        opacity: 0;
    }
    .auth-hero-section:nth-child(1) { animation-delay: 0.05s; }
    .auth-hero-section:nth-child(2) { animation-delay: 0.15s; }
    .auth-hero-section:nth-child(3) { animation-delay: 0.25s; }
    .auth-hero-section:nth-child(4) { animation-delay: 0.35s; }
    .auth-hero-section:nth-child(5) { animation-delay: 0.45s; }
    .auth-hero-section:nth-child(6) { animation-delay: 0.55s; }
    .auth-hero-section:nth-child(7) { animation-delay: 0.65s; }

    .auth-logo-row {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
    }
    .auth-logo-icon {
        width: 44px; height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #C9A86A 0%, #B8954E 100%);
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 8px 32px rgba(201,168,106,0.2);
        position: relative;
        overflow: hidden;
    }
    .auth-logo-icon::after {
        content: ''; position: absolute; inset: 0;
        background: linear-gradient(135deg, transparent 40%, rgba(255,255,255,0.15) 50%, transparent 60%);
        background-size: 200% 200%;
        animation: authGoldShimmer 4s ease-in-out infinite;
    }
    .auth-logo-icon span {
        color: #09090B; font-weight: 800; font-size: 1.35rem; position: relative; z-index: 1;
    }
    .auth-logo-text {
        display: flex; flex-direction: column;
    }
    .auth-logo-name {
        font-size: 1rem; font-weight: 700; color: #FAFAFA; letter-spacing: 0.01em;
    }
    .auth-logo-sub {
        font-size: 0.72rem; color: #71717A; font-weight: 500; letter-spacing: 0.04em;
    }

    .auth-heading {
        margin: 32px 0 16px;
    }
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

    /* ── Feature Cards ─────────────────────────────────────── */
    .auth-features {
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        margin-bottom: 44px;
    }
    .auth-fcard {
        flex: 1 1 140px;
        min-width: 130px;
        max-width: 180px;
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
        width: 32px; height: 32px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 10px;
        font-size: 0.85rem;
    }
    .auth-fcard-title {
        font-size: 0.8rem;
        font-weight: 600;
        color: #FAFAFA;
        margin: 0 0 3px;
    }
    .auth-fcard-desc {
        font-size: 0.68rem;
        color: #52525B;
        margin: 0;
        line-height: 1.4;
    }
    .auth-fcard:hover .auth-fcard-desc {
        color: #71717A;
    }

    /* ── Dashboard Preview ─────────────────────────────────── */
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
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
    }
    .auth-preview-top-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .auth-preview-top-left span {
        font-size: 0.78rem;
        color: #A1A1AA;
        font-weight: 500;
    }
    .auth-preview-live {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-size: 0.62rem;
        font-weight: 700;
        color: #22C55E;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 3px 10px;
        border-radius: 20px;
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.12);
    }
    .auth-preview-live-dot {
        width: 5px; height: 5px;
        border-radius: 50%;
        background: #22C55E;
        animation: authPulse 2s ease-in-out infinite;
    }
    .auth-preview-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }
    .auth-preview-metric {
        background: rgba(255,255,255,0.02);
        border-radius: 14px;
        padding: 14px 16px;
        border: 1px solid rgba(255,255,255,0.03);
    }
    .auth-preview-metric-label {
        font-size: 0.68rem;
        color: #52525B;
        font-weight: 500;
        margin-bottom: 4px;
    }
    .auth-preview-metric-value {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FAFAFA;
    }
    .auth-preview-metric-value.gold { color: #C9A86A; }
    .auth-preview-metric-value.green { color: #22C55E; }
    .auth-preview-metric-value.purple { color: #A855F7; }
    .auth-preview-metric-value.blue { color: #3B82F6; }
    .auth-preview-chart {
        display: flex;
        align-items: flex-end;
        gap: 4px;
        height: 36px;
        margin-top: 8px;
    }
    .auth-preview-chart-bar {
        flex: 1;
        border-radius: 3px 3px 0 0;
        min-height: 4px;
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
        margin-top: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.03);
    }
    .auth-preview-bottom-item {
        text-align: center;
    }
    .auth-preview-bottom-item .val {
        font-size: 0.82rem;
        font-weight: 700;
        color: #FAFAFA;
    }
    .auth-preview-bottom-item .lbl {
        font-size: 0.6rem;
        color: #52525B;
        font-weight: 500;
        margin-top: 2px;
    }
    .auth-preview-svg-line {
        width: 100%;
        height: 100%;
    }
    .auth-preview-svg-line path {
        stroke-dasharray: 200;
        stroke-dashoffset: 200;
        animation: authDrawLine 2s ease-out 0.5s forwards;
    }
    @keyframes authDrawLine {
        to { stroke-dashoffset: 0; }
    }

    /* ── Statistics Row ────────────────────────────────────── */
    .auth-stats {
        display: flex;
        gap: 28px;
        flex-wrap: wrap;
        margin-bottom: 36px;
    }
    .auth-stat {
        display: flex;
        flex-direction: column;
    }
    .auth-stat-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #FAFAFA;
        letter-spacing: -0.02em;
        line-height: 1;
    }
    .auth-stat-value.gold { color: #C9A86A; }
    .auth-stat-label {
        font-size: 0.7rem;
        color: #52525B;
        font-weight: 500;
        margin-top: 3px;
    }

    /* ── Social Proof ──────────────────────────────────────── */
    .auth-social {
        display: flex;
        align-items: center;
        gap: 28px;
        flex-wrap: wrap;
        padding-bottom: 8px;
    }
    .auth-social-label {
        font-size: 0.65rem;
        color: #3F3F46;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .auth-social-name {
        font-size: 0.8rem;
        color: #3F3F46;
        font-weight: 500;
        letter-spacing: 0.02em;
        transition: color 0.25s ease;
    }
    .auth-social-name:hover {
        color: #71717A;
    }

    /* ── Right Panel (40%) ──────────────────────────────────── */
    .auth-panel {
        flex: 0 0 40%;
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 48px 64px 48px 40px;
        overflow-y: auto;
        background: rgba(17,17,19,0.85);
        backdrop-filter: blur(4px);
        -webkit-backdrop-filter: blur(4px);
    }
    .auth-panel-inner {
        width: 100%;
        max-width: 460px;
        animation: authScaleIn 0.6s ease-out 0.1s both;
    }

    /* ── Auth Card ─────────────────────────────────────────── */
    .auth-card {
        background: rgba(20,20,24,0.72);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 28px;
        padding: 44px 40px 36px;
        box-shadow: 0 32px 96px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.02) inset;
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
    .auth-card-logo-hex-inner span {
        color: #09090B;
        font-weight: 800;
        font-size: 1rem;
    }

    .auth-card-heading {
        text-align: center;
        margin-bottom: 6px;
    }
    .auth-card-heading h2 {
        font-size: 1.45rem;
        font-weight: 700;
        color: #FAFAFA;
        margin: 0;
        letter-spacing: -0.01em;
    }
    .auth-card-subtitle {
        text-align: center;
        font-size: 0.8rem;
        color: #71717A;
        margin: 0 0 20px;
    }
    .auth-card-divider {
        width: 36px;
        height: 2.5px;
        background: linear-gradient(90deg, #C9A86A, rgba(201,168,106,0.3));
        border-radius: 4px;
        margin: 0 auto 24px;
    }

    .auth-divider-or {
        display: flex;
        align-items: center;
        gap: 16px;
        margin: 16px 0;
    }
    .auth-divider-or-line {
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(201,168,106,0.15), transparent);
    }
    .auth-divider-or-text {
        font-size: 0.7rem;
        color: #52525B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .auth-google-btn {
        width: 100%;
        padding: 13px 20px;
        border-radius: 14px;
        font-weight: 600;
        font-family: 'Manrope', sans-serif;
        font-size: 0.875rem;
        letter-spacing: 0.01em;
        background: #FAFAFA;
        color: #09090B;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
        box-shadow: 0 4px 24px rgba(255,255,255,0.08);
    }
    .auth-google-btn:hover {
        box-shadow: 0 8px 40px rgba(255,255,255,0.12);
        transform: translateY(-2px);
    }
    .auth-google-btn:active { transform: scale(0.97); }

    .auth-email-btn {
        width: 100%;
        padding: 13px 20px;
        border-radius: 14px;
        font-weight: 600;
        font-family: 'Manrope', sans-serif;
        font-size: 0.875rem;
        letter-spacing: 0.01em;
        background: transparent;
        color: #C9A86A;
        border: 1.5px solid rgba(201,168,106,0.3);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
        box-shadow: none;
    }
    .auth-email-btn:hover {
        border-color: #C9A86A;
        box-shadow: 0 0 40px rgba(201,168,106,0.1), inset 0 0 20px rgba(201,168,106,0.03);
        transform: translateY(-2px);
        color: #D4B47A;
    }
    .auth-email-btn:active { transform: scale(0.97); }
    .auth-email-btn .icon { font-size: 1rem; }

    .auth-back-btn {
        width: 100%;
        padding: 13px 20px;
        border-radius: 14px;
        font-weight: 600;
        font-family: 'Manrope', sans-serif;
        font-size: 0.875rem;
        background: transparent;
        color: #A1A1AA;
        border: 1px solid rgba(255,255,255,0.08);
        cursor: pointer;
        transition: all 0.25s ease;
    }
    .auth-back-btn:hover {
        background: rgba(255,255,255,0.03);
        border-color: rgba(201,168,106,0.2);
        color: #FAFAFA;
    }

    /* ── Security Row ──────────────────────────────────────── */
    .auth-security {
        display: flex;
        gap: 8px;
        margin: 22px 0 18px;
        justify-content: center;
    }
    .auth-security-item {
        flex: 1;
        text-align: center;
        padding: 10px 6px;
        border-radius: 12px;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.03);
        transition: all 0.25s ease;
    }
    .auth-security-item:hover {
        background: rgba(255,255,255,0.04);
        border-color: rgba(255,255,255,0.06);
    }
    .auth-security-icon {
        font-size: 1rem;
        margin-bottom: 4px;
    }
    .auth-security-title {
        font-size: 0.62rem;
        font-weight: 600;
        color: #A1A1AA;
        margin: 0;
    }
    .auth-security-desc {
        font-size: 0.55rem;
        color: #52525B;
        margin: 1px 0 0;
        line-height: 1.2;
    }

    /* ── Card Footer ───────────────────────────────────────── */
    .auth-card-footer {
        text-align: center;
        margin-top: 6px;
    }
    .auth-card-footer p {
        font-size: 0.68rem;
        color: #52525B;
        margin: 0;
    }
    .auth-card-footer a {
        color: #C9A86A;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    .auth-card-footer a:hover {
        color: #E8D098;
        text-decoration: underline;
    }

    .auth-enterprise {
        text-align: center;
        margin-top: 16px;
    }
    .auth-enterprise span {
        font-size: 0.62rem;
        color: #3F3F46;
        font-weight: 500;
        letter-spacing: 0.02em;
    }
    .auth-enterprise-sep {
        margin: 0 8px;
        color: #3F3F46;
    }

    /* ── Auth Flow Pages (email & otp) ──────────────────────── */
    .auth-flow-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .auth-flow-header .icon-wrap {
        width: 44px; height: 44px;
        border-radius: 14px;
        margin: 0 auto 12px;
        display: flex; align-items: center; justify-content: center;
    }
    .auth-flow-header h3 {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FAFAFA;
        margin: 0 0 2px;
    }
    .auth-flow-header p {
        font-size: 0.78rem;
        color: #71717A;
        margin: 0;
    }

    .auth-flow-back-row {
        display: flex; align-items: center; gap: 6px;
        font-size: 0.78rem; color: #71717A;
        cursor: pointer; padding: 6px 12px 6px 0;
        border-radius: 8px; transition: all 0.2s ease;
        width: fit-content;
        margin-bottom: 12px;
    }
    .auth-flow-back-row:hover { color: #FAFAFA; }

    .auth-sent-box {
        background: rgba(26,24,16,0.7);
        border: 1px solid rgba(201,168,106,0.12);
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin-bottom: 20px;
    }
    .auth-sent-icon {
        width: 44px; height: 44px;
        border-radius: 50%;
        background: rgba(201,168,106,0.08);
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 8px;
    }
    .auth-sent-icon svg { stroke: #C9A86A; }
    .auth-sent-check {
        font-size: 0.78rem; color: #22C55E; font-weight: 500;
        display: inline-flex; align-items: center; gap: 4px;
    }
    .auth-sent-hint {
        font-size: 0.68rem; color: #52525B; margin: 4px 0 0;
    }

    /* ── Responsive ────────────────────────────────────────── */
    @media (max-width: 1200px) {
        .auth-hero { padding: 40px 40px 40px 48px; }
        .auth-panel { padding: 40px 40px 40px 24px; }
        .auth-card { padding: 36px 32px 32px; }
        .auth-preview-grid { gap: 12px; }
    }
    @media (max-width: 1024px) {
        .auth-split { flex-direction: column; overflow-y: auto; position: relative; min-height: 100vh; }
        .auth-bg { position: fixed; }
        .auth-hero { flex: none; padding: 40px 32px 24px; min-height: auto; }
        .auth-hero-inner { max-width: 100%; }
        .auth-heading h1 { font-size: clamp(2.2rem, 6vw, 3.2rem); }
        .auth-features { gap: 10px; }
        .auth-fcard { flex: 1 1 120px; min-width: 110px; max-width: none; padding: 14px 12px; }
        .auth-preview { max-width: 100%; }
        .auth-panel { flex: none; padding: 16px 32px 32px; }
        .auth-panel-inner { max-width: 460px; margin: 0 auto; }
        .auth-stats { gap: 20px; }
        .auth-stat-value { font-size: 1.4rem; }
    }
    @media (max-width: 640px) {
        .auth-hero { padding: 28px 20px 16px; }
        .auth-panel { padding: 12px 20px 28px; }
        .auth-card { padding: 28px 22px 24px; border-radius: 22px; }
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
