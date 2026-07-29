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
