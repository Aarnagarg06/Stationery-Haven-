import streamlit as st
import time

# Page config
st.set_page_config(
    page_title="Enterprise Stock Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for luxury enterprise design
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 80px 20px 60px 20px;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.05) 0%, rgba(0, 188, 212, 0.05) 100%);
        border-radius: 20px;
        margin-bottom: 60px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #d4af37 0%, #ffffff 50%, #00bcd4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 20px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #b0b0b0;
        font-weight: 300;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 8px 24px;
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 50px;
        color: #d4af37;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1px;
        margin-top: 20px;
    }
    
    /* Role Cards Grid */
    .cards-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 30px;
        padding: 0 20px 60px 20px;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Glassmorphism Card */
    .role-card {
        background: rgba(42, 42, 42, 0.4);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 40px 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        text-align: center;
    }
    
    .role-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(0, 188, 212, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .role-card:hover {
        transform: translateY(-10px);
        border-color: rgba(212, 175, 55, 0.4);
        box-shadow: 0 16px 48px rgba(212, 175, 55, 0.2),
                    0 0 40px rgba(0, 188, 212, 0.1);
    }
    
    .role-card:hover::before {
        opacity: 1;
    }
    
    .card-icon {
        font-size: 3.5rem;
        margin-bottom: 20px;
        filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
        position: relative;
        z-index: 1;
    }
    
    .card-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 12px;
        position: relative;
        z-index: 1;
    }
    
    .card-description {
        font-size: 0.95rem;
        color: #b0b0b0;
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    .card-accent {
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #d4af37, #00bcd4);
        margin: 20px auto;
        border-radius: 2px;
        position: relative;
        z-index: 1;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 40px 20px;
        color: #666;
        font-size: 0.85rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 40px;
    }
    
    .footer-text {
        margin-bottom: 8px;
        letter-spacing: 1px;
    }
    
    .footer-version {
        color: #d4af37;
        font-weight: 600;
    }
    
    /* Streamlit Button Override */
    .stButton > button {
        background: transparent;
        border: none;
        padding: 0;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: transparent;
        border: none;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.2rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
        .cards-container {
            grid-template-columns: 1fr;
            padding: 0 10px 40px 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-title">
        ENTERPRISE STOCK MANAGEMENT
    </div>
    <div class="hero-subtitle">
        Precision · Control · Performance
    </div>
    <div class="hero-badge">
        🔐 SECURE ACCESS ONLY
    </div>
</div>
""", unsafe_allow_html=True)

# Role Cards Section
st.markdown('<div class="cards-container">', unsafe_allow_html=True)

# Create 4 columns for the role cards
col1, col2, col3, col4 = st.columns(4)

# Role 1: Clerk
with col1:
    if st.button("clerk_btn", key="clerk", use_container_width=True):
        st.session_state.selected_role = "Clerk"
        st.rerun()
    
    st.markdown("""
    <div class="role-card">
        <div class="card-icon">🧾</div>
        <div class="card-title">Clerk</div>
        <div class="card-accent"></div>
        <div class="card-description">
            Manage daily stock entries, transactions, and record-keeping operations
        </div>
    </div>
    """, unsafe_allow_html=True)

# Role 2: Inventory Manager
with col2:
    if st.button("manager_btn", key="manager", use_container_width=True):
        st.session_state.selected_role = "Inventory Manager"
        st.rerun()
    
    st.markdown("""
    <div class="role-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Inventory Manager</div>
        <div class="card-accent"></div>
        <div class="card-description">
            Oversee stock levels, analytics, and comprehensive reporting dashboards
        </div>
    </div>
    """, unsafe_allow_html=True)

# Role 3: Auditor
with col3:
    if st.button("auditor_btn", key="auditor", use_container_width=True):
        st.session_state.selected_role = "Auditor"
        st.rerun()
    
    st.markdown("""
    <div class="role-card">
        <div class="card-icon">🧠</div>
        <div class="card-title">Auditor</div>
        <div class="card-accent"></div>
        <div class="card-description">
            Verify records, ensure compliance, and maintain data integrity standards
        </div>
    </div>
    """, unsafe_allow_html=True)

# Role 4: Admin
with col4:
    if st.button("admin_btn", key="admin", use_container_width=True):
        st.session_state.selected_role = "Administrator"
        st.rerun()
    
    st.markdown("""
    <div class="role-card">
        <div class="card-icon">🏢</div>
        <div class="card-title">Administrator</div>
        <div class="card-accent"></div>
        <div class="card-description">
            System configuration, user management, and access control operations
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="custom-footer">
    <div class="footer-text">
        Powered by <strong>Enterprise Solutions™</strong> | Secure Access Only
    </div>
    <div class="footer-version">
        Version 1.0 | Build 2024.12
    </div>
</div>
""", unsafe_allow_html=True)

# Handle navigation (placeholder for role pages)
if 'selected_role' in st.session_state:
    st.info(f"🎯 Navigation: {st.session_state.selected_role} Dashboard (Page under development)")
    if st.button("← Return to Home"):
        del st.session_state.selected_role
        st.rerun()
        