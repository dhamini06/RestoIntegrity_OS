import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Poppins', sans-serif !important;
            background: linear-gradient(135deg, #faf5ff 0%, #f0f9ff 30%, #ecfdf5 60%, #fff7ed 100%) !important;
            color: #1e293b !important;
        }

        .main .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
            border-right: 2px solid rgba(99, 102, 241, 0.1) !important;
            box-shadow: 4px 0 30px rgba(99, 102, 241, 0.08) !important;
        }
        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem !important;
        }

        [data-testid="stHeader"] { display: none !important; }
        div[data-testid="stToolbar"] { display: none !important; }
        footer { display: none !important; visibility: hidden !important; }
        #MainMenu { display: none !important; visibility: hidden !important; }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #6366f1, #8b5cf6); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #4f46e5, #7c3aed); }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 15px rgba(99, 102, 241, 0.2); }
            50% { box-shadow: 0 0 30px rgba(99, 102, 241, 0.4); }
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
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1.5px solid rgba(99, 102, 241, 0.12);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.5s ease-out;
        }
        .glass-card:hover {
            border-color: rgba(99, 102, 241, 0.25);
            box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
            transform: translateY(-3px);
        }

        .fun-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.6));
            border: 2px solid transparent;
            border-image: linear-gradient(135deg, #6366f1, #ec4899, #f59e0b) 1;
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 20px;
            animation: bounceIn 0.6s ease-out;
        }

        .gradient-text {
            background: linear-gradient(135deg, #6366f1, #ec4899, #f59e0b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .glow-indigo {
            color: #6366f1 !important;
            text-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        }
        .glow-pink {
            color: #ec4899 !important;
            text-shadow: 0 0 20px rgba(236, 72, 153, 0.3);
        }
        .glow-amber {
            color: #f59e0b !important;
            text-shadow: 0 0 20px rgba(245, 158, 11, 0.3);
        }
        .glow-emerald {
            color: #10b981 !important;
            text-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }
        .glow-red {
            color: #ef4444 !important;
            text-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
        }

        button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-family: 'Poppins', sans-serif !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: none !important;
        }

        button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: white !important;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.35) !important;
            padding: 10px 24px !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 6px 30px rgba(99, 102, 241, 0.5) !important;
            transform: translateY(-2px) scale(1.02) !important;
        }

        button[kind="secondary"] {
            background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08)) !important;
            color: #6366f1 !important;
            border: 1.5px solid rgba(99, 102, 241, 0.2) !important;
        }
        button[kind="secondary"]:hover {
            background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15)) !important;
            border-color: rgba(99, 102, 241, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.6) !important;
            border: 1.5px solid rgba(99, 102, 241, 0.1) !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.06) !important;
            margin-bottom: 12px !important;
            backdrop-filter: blur(10px) !important;
        }
        div[data-testid="stExpander"] summary {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            color: #6366f1 !important;
            font-size: 0.95rem !important;
        }
        div[data-testid="stExpander"] summary:hover {
            color: #4f46e5 !important;
        }

        .metric-value {
            font-family: 'Poppins', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            margin: 5px 0;
            background: linear-gradient(135deg, #6366f1, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .metric-value-amber {
            font-family: 'Poppins', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            margin: 5px 0;
            background: linear-gradient(135deg, #f59e0b, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .metric-value-emerald {
            font-family: 'Poppins', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            margin: 5px 0;
            background: linear-gradient(135deg, #10b981, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .alert-card-high {
            border-left: 5px solid #ef4444;
            background: linear-gradient(135deg, rgba(239,68,68,0.04), rgba(239,68,68,0.01));
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(239, 68, 68, 0.06);
            animation: slideInLeft 0.4s ease-out;
            transition: all 0.3s ease;
        }
        .alert-card-high:hover {
            box-shadow: 0 8px 30px rgba(239, 68, 68, 0.12);
            transform: translateX(4px);
        }
        .alert-card-medium {
            border-left: 5px solid #f59e0b;
            background: linear-gradient(135deg, rgba(245,158,11,0.04), rgba(245,158,11,0.01));
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(245, 158, 11, 0.06);
            animation: slideInLeft 0.4s ease-out;
            transition: all 0.3s ease;
        }
        .alert-card-medium:hover {
            box-shadow: 0 8px 30px rgba(245, 158, 11, 0.12);
            transform: translateX(4px);
        }
        .alert-card-low {
            border-left: 5px solid #10b981;
            background: linear-gradient(135deg, rgba(16,185,129,0.04), rgba(16,185,129,0.01));
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(16, 185, 129, 0.06);
            animation: slideInLeft 0.4s ease-out;
        }

        input[type="text"], input[type="password"], div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.8) !important;
            border: 1.5px solid rgba(99, 102, 241, 0.15) !important;
            border-radius: 12px !important;
            color: #1e293b !important;
            font-family: 'Poppins', sans-serif !important;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
        }

        div[role="radiogroup"] {
            display: flex !important;
            flex-direction: column !important;
            gap: 8px !important;
            margin-top: 12px !important;
        }
        div[role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.6) !important;
            border: 1.5px solid rgba(99, 102, 241, 0.1) !important;
            border-radius: 14px !important;
            padding: 12px 16px !important;
            color: #64748b !important;
            cursor: pointer !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            font-family: 'Poppins', sans-serif !important;
            font-weight: 500 !important;
        }
        div[role="radiogroup"] label:hover {
            background: rgba(99, 102, 241, 0.06) !important;
            border-color: rgba(99, 102, 241, 0.3) !important;
            color: #6366f1 !important;
            transform: translateX(4px);
        }
        div[role="radiogroup"] label:has(input[type="radio"]:checked) {
            background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1)) !important;
            border-color: #6366f1 !important;
            color: #6366f1 !important;
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.12) !important;
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
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-family: 'Poppins', sans-serif;
        }
        .badge-critical {
            background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.08));
            color: #dc2626;
            border: 1px solid rgba(239,68,68,0.3);
            animation: pulse-glow 2s infinite;
        }
        .badge-medium {
            background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(245,158,11,0.08));
            color: #d97706;
            border: 1px solid rgba(245,158,11,0.3);
        }
        .badge-low {
            background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.08));
            color: #059669;
            border: 1px solid rgba(16,185,129,0.3);
        }
        .badge-indigo {
            background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(99,102,241,0.08));
            color: #4f46e5;
            border: 1px solid rgba(99,102,241,0.3);
        }
        .badge-pink {
            background: linear-gradient(135deg, rgba(236,72,153,0.15), rgba(236,72,153,0.08));
            color: #db2777;
            border: 1px solid rgba(236,72,153,0.3);
        }

        .tip-highlight {
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border: 2px solid #f59e0b;
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            animation: bounceIn 0.5s ease-out;
        }

        div[data-testid="stTabs"] button {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            padding: 10px 20px !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            color: white !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        }

        .stale-badge {
            background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(239,68,68,0.1)) !important;
            color: #dc2626 !important;
            border: 2px solid rgba(239,68,68,0.4) !important;
            animation: pulse-glow 1.5s infinite !important;
            font-weight: 700 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def show_glass_card(title, content_html, icon="", color="indigo"):
    color_class = f"glow-{color}"
    st.markdown(f"""
        <div class="glass-card">
            <h4 class="{color_class}">{icon} {title}</h4>
            <div style="margin-top: 10px;">
                {content_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_metric_card(label, value, icon="", color="indigo"):
    val_class = f"metric-value" if color == "indigo" else f"metric-value-{color}"
    st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:20px;">
            <div style="font-size:1.8rem;">{icon}</div>
            <div style="font-size:0.85rem; color:#64748b; font-weight:500; margin-top:4px;">{label}</div>
            <div class="{val_class}">{value}</div>
        </div>
    """, unsafe_allow_html=True)
