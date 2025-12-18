# ==========================================
# LUXURY ENTERPRISE LANDING PAGE
# File: landing.py
# ==========================================

import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* ---------- GOOGLE FONT ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0f1419;
        color: #ffffff;
    }

    /* ---------- HERO SECTION ---------- */
    .hero {
        padding: 5rem 4rem;
        border-radius: 24px;
        background: linear-gradient(
            135deg,
            rgba(212,175,55,0.12),
            rgba(15,20,25,1)
        );
        box-shadow: 0 40px 80px rgba(0,0,0,0.7);
        margin-bottom: 4rem;
    }

    .hero h1 {
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
    }

    .hero p {
        font-size: 1.25rem;
        color: #b0b0b0;
    }

    /* ---------- ROLE CARDS ---------- */
    .card {
        background: rgba(42,42,42,0.55);
        backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 2.4rem;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.35s ease;
        height: 100%;
    }

    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 60px rgba(212,175,55,0.35);
        border: 1px solid rgba(212,175,55,0.6);
    }

    .card h3 {
        font-size: 1.4rem;
        margin-bottom: 0.5rem;
    }

    .card p {
        font-size: 0.95rem;
        color: #b0b0b0;
        line-height: 1.5;
    }

    .lux-btn {
        margin-top: 1.5rem;
        padding: 0.6rem 1.8rem;
        border-radius: 999px;
        background: linear-gradient(90deg, #d4af37, #f5d76e);
        color: #000;
        font-weight: 700;
        border: none;
    }

    /* ---------- FOOTER ---------- */
    .footer {
        margin-top: 6rem;
        text-align: center;
        color: #777;
        font-size: 0.85rem;
    }

    </style>
    """, unsafe_allow_html=True)


def landing_page():
    load_css()

    # HERO
    st.markdown("""
    <div class="hero">
        <h1>Enterprise Stock Management System</h1>
        <p>Precision. Control. Performance.</p>
    </div>
    """, unsafe_allow_html=True)

    # ROLE CARDS
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>🧾 Clerk</h3>
            <p>Manage daily stock entries with operational accuracy and traceability.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Workspace", key="clerk"):
            st.session_state["role"] = "Clerk"
            st.session_state["page"] = "app"

    with col2:
        st.markdown("""
        <div class="card">
            <h3>📊 Inventory Manager</h3>
            <p>Oversee stock levels, movement analytics, and inventory health.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Access Dashboard", key="manager"):
            st.session_state["role"] = "Manager"
            st.session_state["page"] = "app"

    with col3:
        st.markdown("""
        <div class="card">
            <h3>🧠 Auditor</h3>
            <p>Validate records, compliance, and financial integrity of inventory.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Reports", key="auditor"):
            st.session_state["role"] = "Auditor"
            st.session_state["page"] = "app"

    with col4:
        st.markdown("""
        <div class="card">
            <h3>🏢 Administrator</h3>
            <p>Enterprise configuration, access control, and system governance.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Admin Console", key="admin"):
            st.session_state["role"] = "Admin"
            st.session_state["page"] = "app"

    # FOOTER
    st.markdown("""
    <div class="footer">
        Powered by ApexCorp Systems | Secure Internal Access Only <br>
        Version 1.0
    </div>
    """, unsafe_allow_html=True)
