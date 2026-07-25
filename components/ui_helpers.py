import streamlit as st

def inject_custom_css():
    """
    Injects global CSS styles to give the Streamlit application a premium,
    glassmorphic, dark-mode cybersecurity feel.
    """
    st.markdown("""
        <style>
        /* Base styles */
        .stApp {
            background: linear-gradient(135deg, #0f0f1b 0%, #15102a 50%, #0a0815 100%);
            color: #e2e8f0;
            font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Glassmorphic Container */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.3s ease;
        }
        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }
        
        /* Glow titles */
        .glow-text-cyan {
            color: #00f2fe;
            text-shadow: 0 0 10px rgba(0, 242, 254, 0.4);
            font-weight: 700;
        }
        .glow-text-purple {
            color: #b927fc;
            text-shadow: 0 0 10px rgba(185, 39, 252, 0.4);
            font-weight: 700;
        }
        .glow-text-amber {
            color: #ff9f43;
            text-shadow: 0 0 10px rgba(255, 159, 67, 0.4);
            font-weight: 700;
        }
        .glow-text-red {
            color: #ff4d4d;
            text-shadow: 0 0 10px rgba(255, 77, 77, 0.4);
            font-weight: 700;
        }
        
        /* Dashboard metric styling */
        .metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            margin: 5px 0;
            background: linear-gradient(90deg, #00f2fe, #4facfe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Alert Feed Banner Cards */
        .alert-card-high {
            border-left: 6px solid #ff4d4d;
            background: rgba(255, 77, 77, 0.04);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 12px;
            border-top: 1px solid rgba(255, 77, 77, 0.1);
            border-right: 1px solid rgba(255, 77, 77, 0.1);
            border-bottom: 1px solid rgba(255, 77, 77, 0.1);
        }
        .alert-card-medium {
            border-left: 6px solid #ff9f43;
            background: rgba(255, 159, 67, 0.04);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 12px;
            border-top: 1px solid rgba(255, 159, 67, 0.1);
            border-right: 1px solid rgba(255, 159, 67, 0.1);
            border-bottom: 1px solid rgba(255, 159, 67, 0.1);
        }
        
        /* Badges */
        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-critical { background-color: rgba(255, 77, 77, 0.2); color: #ff4d4d; border: 1px solid #ff4d4d; }
        .badge-medium { background-color: rgba(255, 159, 67, 0.2); color: #ff9f43; border: 1px solid #ff9f43; }
        .badge-low { background-color: rgba(0, 242, 254, 0.2); color: #00f2fe; border: 1px solid #00f2fe; }
        
        /* Form inputs and buttons styling */
        div[data-baseweb="select"] {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
        }
        input {
            background-color: rgba(255, 255, 255, 0.02) !important;
            color: white !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Hide default Streamlit decoration */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
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
