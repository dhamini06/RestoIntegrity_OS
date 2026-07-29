import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif !important;
            background: #FFFDF6 !important;
            color: #2C1810 !important;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif !important;
            font-weight: 700 !important;
            color: #2C1810 !important;
        }

        .main .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px !important;
        }

        [data-testid="stSidebar"] {
            background: #FFFAF5 !important;
            border-right: 1px solid #E8D5A3 !important;
            box-shadow: 4px 0 30px rgba(197, 165, 90, 0.08) !important;
        }
        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem !important;
        }

        [data-testid="stHeader"] { display: none !important; }
        div[data-testid="stToolbar"] { display: none !important; }
        footer { display: none !important; visibility: hidden !important; }
        #MainMenu { display: none !important; visibility: hidden !important; }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #F8F3E9; border-radius: 10px; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #C5A55A, #A68332); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #A68332, #8B6914); }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes bounceIn {
            0% { transform: scale(0.9); opacity: 0; }
            60% { transform: scale(1.02); }
            100% { transform: scale(1); opacity: 1; }
        }

        .glass-card {
            background: #FFFFFF;
            border: 1px solid #E8D5A3;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 24px rgba(197, 165, 90, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.5s ease-out;
        }
        .glass-card:hover {
            border-color: #C5A55A;
            box-shadow: 0 8px 32px rgba(197, 165, 90, 0.15);
            transform: translateY(-2px);
        }

        .fun-card {
            background: linear-gradient(135deg, #FFFFFF, #FFFDF6);
            border: 1.5px solid #E8D5A3;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            animation: bounceIn 0.6s ease-out;
        }

        .gradient-text {
            background: linear-gradient(135deg, #C5A55A, #8B6914);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .glow-gold {
            color: #C5A55A !important;
            text-shadow: 0 0 20px rgba(197, 165, 90, 0.2);
        }
        .glow-amber {
            color: #B8860B !important;
            text-shadow: 0 0 20px rgba(184, 134, 11, 0.2);
        }
        .glow-emerald {
            color: #2E7D32 !important;
            text-shadow: 0 0 20px rgba(46, 125, 50, 0.2);
        }
        .glow-red {
            color: #C62828 !important;
            text-shadow: 0 0 20px rgba(198, 40, 40, 0.2);
        }
        .glow-brown {
            color: #5D4037 !important;
            text-shadow: 0 0 20px rgba(93, 64, 55, 0.2);
        }

        button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: none !important;
        }

        button[kind="primary"] {
            background: linear-gradient(135deg, #C5A55A, #A68332) !important;
            color: white !important;
            box-shadow: 0 4px 20px rgba(197, 165, 90, 0.35) !important;
            padding: 10px 24px !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 6px 30px rgba(197, 165, 90, 0.5) !important;
            transform: translateY(-2px) !important;
        }

        button[kind="secondary"] {
            background: #F8F3E9 !important;
            color: #5D4037 !important;
            border: 1px solid #E8D5A3 !important;
        }
        button[kind="secondary"]:hover {
            background: #F0E6C8 !important;
            border-color: #C5A55A !important;
            transform: translateY(-1px) !important;
        }

        div[data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E8D5A3 !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 20px rgba(197, 165, 90, 0.06) !important;
            margin-bottom: 12px !important;
        }
        div[data-testid="stExpander"] summary {
            font-family: 'Playfair Display', serif !important;
            font-weight: 600 !important;
            color: #5D4037 !important;
            font-size: 1rem !important;
        }
        div[data-testid="stExpander"] summary:hover {
            color: #C5A55A !important;
        }

        .metric-value {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 700;
            margin: 5px 0;
            color: #2C1810;
        }
        .metric-value-amber {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 700;
            margin: 5px 0;
            color: #B8860B;
        }
        .metric-value-emerald {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 700;
            margin: 5px 0;
            color: #2E7D32;
        }

        .alert-card-high {
            border-left: 4px solid #C62828;
            background: #FFF5F5;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(198, 40, 40, 0.06);
            animation: slideInLeft 0.4s ease-out;
            transition: all 0.3s ease;
        }
        .alert-card-high:hover {
            box-shadow: 0 8px 30px rgba(198, 40, 40, 0.12);
            transform: translateX(4px);
        }
        .alert-card-medium {
            border-left: 4px solid #B8860B;
            background: #FFFDF5;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(184, 134, 11, 0.06);
            animation: slideInLeft 0.4s ease-out;
            transition: all 0.3s ease;
        }
        .alert-card-medium:hover {
            box-shadow: 0 8px 30px rgba(184, 134, 11, 0.12);
            transform: translateX(4px);
        }
        .alert-card-low {
            border-left: 4px solid #2E7D32;
            background: #F1F8E9;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(46, 125, 50, 0.06);
            animation: slideInLeft 0.4s ease-out;
        }

        input[type="text"], input[type="password"], input[type="number"], div[data-baseweb="select"] {
            background: #FFFFFF !important;
            border: 1px solid #E0D5C0 !important;
            border-radius: 10px !important;
            color: #2C1810 !important;
            font-family: 'Inter', sans-serif !important;
        }
        input[type="text"]:focus, input[type="password"]:focus, input[type="number"]:focus {
            border-color: #C5A55A !important;
            box-shadow: 0 0 0 3px rgba(197, 165, 90, 0.15) !important;
        }

        div[role="radiogroup"] {
            display: flex !important;
            flex-direction: column !important;
            gap: 8px !important;
            margin-top: 12px !important;
        }
        div[role="radiogroup"] label {
            background: #FFFFFF !important;
            border: 1px solid #E0D5C0 !important;
            border-radius: 12px !important;
            padding: 12px 16px !important;
            color: #8C7A6B !important;
            cursor: pointer !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
        }
        div[role="radiogroup"] label:hover {
            background: #FFFDF6 !important;
            border-color: #C5A55A !important;
            color: #5D4037 !important;
            transform: translateX(4px);
        }
        div[role="radiogroup"] label:has(input[type="radio"]:checked) {
            background: #FFFDF6 !important;
            border-color: #C5A55A !important;
            color: #2C1810 !important;
            box-shadow: 0 0 20px rgba(197, 165, 90, 0.12) !important;
            font-weight: 700 !important;
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
            font-family: 'Inter', sans-serif;
        }
        .badge-critical {
            background: #FFEBEE;
            color: #C62828;
            border: 1px solid #FFCDD2;
        }
        .badge-medium {
            background: #FFF8E1;
            color: #B8860B;
            border: 1px solid #FFE082;
        }
        .badge-low {
            background: #E8F5E9;
            color: #2E7D32;
            border: 1px solid #C8E6C9;
        }
        .badge-gold {
            background: #F8F3E9;
            color: #5D4037;
            border: 1px solid #E8D5A3;
        }

        .tip-highlight {
            background: linear-gradient(135deg, #F8F3E9, #F0E6C8);
            border: 1.5px solid #C5A55A;
            border-radius: 14px;
            padding: 16px;
            text-align: center;
            animation: bounceIn 0.5s ease-out;
        }

        div[data-testid="stTabs"] button {
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
            font-size: 0.85rem !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
            color: #8C7A6B !important;
            border: 1px solid transparent !important;
            transition: all 0.25s ease !important;
        }
        div[data-testid="stTabs"] button:hover {
            color: #5D4037 !important;
            border-color: #E8D5A3 !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #C5A55A, #A68332) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(197, 165, 90, 0.3) !important;
            font-weight: 600 !important;
        }

        .stale-badge {
            background: #FFEBEE !important;
            color: #C62828 !important;
            border: 2px solid #EF9A9A !important;
            font-weight: 700 !important;
        }

        div.stDateInput > div {
            border: 1px solid #E0D5C0 !important;
            border-radius: 10px !important;
        }
        div.stDateInput > div:focus-within {
            border-color: #C5A55A !important;
            box-shadow: 0 0 0 3px rgba(197, 165, 90, 0.15) !important;
        }

        hr {
            border-color: #E8D5A3 !important;
            opacity: 0.5;
        }
        </style>
    """, unsafe_allow_html=True)

def show_glass_card(title, content_html, icon="", color="gold"):
    color_class = f"glow-{color}"
    st.markdown(f"""
        <div class="glass-card">
            <h4 class="{color_class}">{icon} {title}</h4>
            <div style="margin-top: 10px;">
                {content_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_metric_card(label, value, icon="", color="gold"):
    val_class = f"metric-value" if color == "gold" else f"metric-value-{color}"
    st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:20px;">
            <div style="font-size:1.8rem;">{icon}</div>
            <div style="font-size:0.85rem; color:#8C7A6B; font-weight:500; margin-top:4px;">{label}</div>
            <div class="{val_class}">{value}</div>
        </div>
    """, unsafe_allow_html=True)
