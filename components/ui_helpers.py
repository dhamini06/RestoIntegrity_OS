import streamlit as st

def inject_custom_css():
    """
    Injects global CSS styles to give the Streamlit application a premium,
    glassmorphic, dark-mode cybersecurity feel.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');
        
        /* Base styles and fonts override */
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background: linear-gradient(135deg, #090714 0%, #0d0a21 50%, #05040b 100%) !important;
            color: #e2e8f0 !important;
        }
        
        /* Adjust main container spacing */
        .main .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            max-width: 1200px !important;
        }
        
        /* Sidebar Glassmorphic Overrides */
        [data-testid="stSidebar"] {
            background-color: #080612 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5) !important;
        }
        [data-testid="stSidebar"] .block-container {
            padding-top: 2rem !important;
        }
        
        /* Hide Default Streamlit UI branding elements */
        [data-testid="stHeader"] {
            display: none !important;
        }
        div[data-testid="stToolbar"] {
            display: none !important;
        }
        footer {
            display: none !important;
            visibility: hidden !important;
        }
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
        }
        
        /* Premium custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #080612;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.15);
        }
        
        /* Glassmorphic Container */
        .glass-card {
            background: rgba(255, 255, 255, 0.025);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.45);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            border-color: rgba(0, 242, 254, 0.15);
            box-shadow: 0 12px 45px 0 rgba(0, 242, 254, 0.05);
            transform: translateY(-2px);
        }
        
        /* Custom headings */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }
        
        /* Glowing neon text tokens */
        .glow-text-cyan {
            color: #00f2fe !important;
            text-shadow: 0 0 15px rgba(0, 242, 254, 0.25);
        }
        .glow-text-purple {
            color: #d946ef !important;
            text-shadow: 0 0 15px rgba(217, 70, 239, 0.25);
        }
        .glow-text-amber {
            color: #f59e0b !important;
            text-shadow: 0 0 15px rgba(245, 158, 11, 0.25);
        }
        .glow-text-red {
            color: #ef4444 !important;
            text-shadow: 0 0 15px rgba(239, 68, 68, 0.25);
        }
        
        /* Custom buttons styling override */
        button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            font-family: 'Outfit', sans-serif !important;
            transition: all 0.2s ease !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
        }
        
        /* primary button glowing effect */
        button[kind="primary"] {
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
            color: #090714 !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0, 242, 254, 0.25) !important;
        }
        button[kind="primary"]:hover {
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4) !important;
            transform: scale(1.02);
        }
        
        /* secondary button styling */
        button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.03) !important;
            color: #e2e8f0 !important;
        }
        button[kind="secondary"]:hover {
            background: rgba(255, 255, 255, 0.06) !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
        }
        
        /* Custom styling for expanders */
        div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.015) !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
            margin-bottom: 12px !important;
        }
        div[data-testid="stExpander"] summary {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            color: #a0aec0 !important;
            font-size: 0.95rem !important;
        }
        div[data-testid="stExpander"] summary:hover {
            color: #00f2fe !important;
        }
        
        /* Metric values styling override */
        .metric-value {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.4rem;
            font-weight: 700;
            margin: 5px 0;
            background: linear-gradient(90deg, #00f2fe, #b927fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Custom Alert Cards styling */
        .alert-card-high {
            border-left: 5px solid #ef4444;
            background: rgba(239, 68, 68, 0.03);
            border-top: 1px solid rgba(239, 68, 68, 0.08);
            border-right: 1px solid rgba(239, 68, 68, 0.08);
            border-bottom: 1px solid rgba(239, 68, 68, 0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 25px rgba(239, 68, 68, 0.03);
        }
        .alert-card-medium {
            border-left: 5px solid #f59e0b;
            background: rgba(245, 158, 11, 0.03);
            border-top: 1px solid rgba(245, 158, 11, 0.08);
            border-right: 1px solid rgba(245, 158, 11, 0.08);
            border-bottom: 1px solid rgba(245, 158, 11, 0.08);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 25px rgba(245, 158, 11, 0.03);
        }
        
        /* Styled input elements */
        input[type="text"], input[type="password"], div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 8px !important;
            color: #f7fafc !important;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #00f2fe !important;
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.2) !important;
        }
        
        /* Transform st.radio group into premium selection cards */
        div[role="radiogroup"] {
            display: flex !important;
            flex-direction: column !important;
            gap: 10px !important;
            margin-top: 15px !important;
        }
        div[role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            color: #a0aec0 !important;
            cursor: pointer !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
        }
        div[role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.05) !important;
            border-color: rgba(0, 242, 254, 0.2) !important;
            color: #00f2fe !important;
            transform: translateX(4px);
        }
        div[role="radiogroup"] label:has(input[type="radio"]:checked) {
            background: rgba(0, 242, 254, 0.06) !important;
            border-color: #00f2fe !important;
            color: #00f2fe !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.15) !important;
            font-weight: 600 !important;
        }
        /* Hide the native round radio button check circles */
        div[role="radiogroup"] label input[type="radio"] {
            display: none !important;
        }
        div[role="radiogroup"] label div[class*="st-"] {
            display: none !important;
        }
        div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
            margin-left: 0 !important;
            padding: 0 !important;
        }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .badge-critical { background-color: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
        .badge-medium { background-color: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .badge-low { background-color: rgba(6, 182, 212, 0.15); color: #22d3ee; border: 1px solid rgba(6, 182, 212, 0.3); }
        </style>
    """, unsafe_allow_html=True)

def show_glass_card(title, content_html, glow_color="cyan"):
    """
    Renders a premium glassmorphic layout card.
    """
    st.markdown(f"""
        <div class="glass-card">
            <h4 class="glow-text-{glow_color}">{title}</h4>
            <div style="margin-top: 10px;">
                {content_html}
            </div>
        </div>
    """, unsafe_allow_html=True)
