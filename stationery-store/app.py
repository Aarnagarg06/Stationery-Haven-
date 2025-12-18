import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Stationery Haven",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Blue & White theme
st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1565c0 0%, #1976d2 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
        color: #ffffff;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e3f2fd;
        text-align: center;
        font-size: 14px;
    }
    
    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > label {
        display: none;
    }
    
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        background: transparent;
        padding: 5px;
    }
    
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.15);
        padding: 12px 20px;
        border-radius: 12px;
        margin: 5px 0;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        font-weight: 500;
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: translateX(5px);
    }
    
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
        background-color: white !important;
        border-color: #ffffff !important;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(21, 101, 192, 0.15);
        text-align: center;
        margin: 10px 0;
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(21, 101, 192, 0.25);
    }
    
    .metric-card h3 {
        margin: 0;
        font-size: 16px;
        color: #1565c0;
        font-weight: 600;
    }
    
    .metric-card h1 {
        margin: 10px 0 0 0;
        font-size: 36px;
        color: #0d47a1;
        font-weight: bold;
    }
    
    /* Title styling */
    h1 {
        color: #1565c0;
        font-weight: bold;
    }
    
    h2, h3 {
        color: #1565c0;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(21, 101, 192, 0.25);
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #90caf9;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #1976d2;
        box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 12px;
        padding: 12px;
        font-weight: 600;
        color: #1565c0;
    }
    
    /* Chart container */
    .plot-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(21, 101, 192, 0.08);
    }
    
    /* Remove top padding */
    .block-container {
        padding-top: 2rem;
    }
    
    /* Branding footer */
    .branding-footer {
        text-align: center;
        color: #1976d2;
        font-size: 12px;
        margin-top: 30px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Database setup and functions
def init_db():
    """Initialize SQLite database with tables"""
    conn = sqlite3.connect('stationery_haven.db', check_same_thread=False)
    c = conn.cursor()
    
    # Products table
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  category TEXT NOT NULL,
                  stock INTEGER NOT NULL,
                  price REAL NOT NULL,
                  supplier TEXT NOT NULL)''')
    
    # Staff table
    c.execute('''CREATE TABLE IF NOT EXISTS staff
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  role TEXT NOT NULL,
                  email TEXT NOT NULL,
                  phone TEXT NOT NULL)''')
    
    # Customers table
    c.execute('''CREATE TABLE IF NOT EXISTS customers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  total_purchases REAL DEFAULT 0)''')
    
    conn.commit()
    return conn

# Initialize database connection
if 'db_conn' not in st.session_state:
    st.session_state.db_conn = init_db()
    
    # Insert demo data if tables are empty
    c = st.session_state.db_conn.cursor()
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        demo_products = [
            ('Gel Pen', 'Pens', 150, 25, 'PenCo'),
            ('Notebook A4', 'Notebooks', 200, 80, 'PaperMill'),
            ('Highlighter Set', 'Markers', 75, 120, 'ColorPro'),
            ('Stapler', 'Accessories', 50, 150, 'OfficeMax'),
            ('Sticky Notes', 'Paper', 300, 40, 'NoteIt'),
            ('Pencil Box', 'Accessories', 100, 90, 'StoragePlus')
        ]
        c.executemany("INSERT INTO products (name, category, stock, price, supplier) VALUES (?, ?, ?, ?, ?)", demo_products)
        
        demo_staff = [
            ('Rajesh Kumar', 'Store Manager', 'rajesh@stationeryhaven.com', '9876543210'),
            ('Priya Sharma', 'Sales Associate', 'priya@stationeryhaven.com', '9876543211'),
            ('Amit Patel', 'Inventory Manager', 'amit@stationeryhaven.com', '9876543212'),
            ('Sneha Reddy', 'Cashier', 'sneha@stationeryhaven.com', '9876543213')
        ]
        c.executemany("INSERT INTO staff (name, role, email, phone) VALUES (?, ?, ?, ?)", demo_staff)
        
        demo_customers = [
            ('Vikram Singh', 'vikram@email.com', '9123456789', 2500),
            ('Anjali Mehta', 'anjali@email.com', '9123456790', 3200),
            ('Rohan Desai', 'rohan@email.com', '9123456791', 1800),
            ('Kavya Iyer', 'kavya@email.com', '9123456792', 4100)
        ]
        c.executemany("INSERT INTO customers (name, email, phone, total_purchases) VALUES (?, ?, ?, ?)", demo_customers)
        
        st.session_state.db_conn.commit()

# Database helper functions
def get_products():
    """Fetch all products from database"""
    return pd.read_sql_query("SELECT * FROM products", st.session_state.db_conn)

def get_staff():
    """Fetch all staff from database"""
    return pd.read_sql_query("SELECT * FROM staff", st.session_state.db_conn)

def get_customers():
    """Fetch all customers from database"""
    return pd.read_sql_query("SELECT * FROM customers", st.session_state.db_conn)

def add_product(name, category, stock, price, supplier):
    """Add new product to database"""
    c = st.session_state.db_conn.cursor()
    c.execute("INSERT INTO products (name, category, stock, price, supplier) VALUES (?, ?, ?, ?, ?)",
              (name, category, stock, price, supplier))
    st.session_state.db_conn.commit()

def update_product(id, name, category, stock, price, supplier):
    """Update existing product in database"""
    c = st.session_state.db_conn.cursor()
    c.execute("UPDATE products SET name=?, category=?, stock=?, price=?, supplier=? WHERE id=?",
              (name, category, stock, price, supplier, id))
    st.session_state.db_conn.commit()

def delete_product(id):
    """Delete product from database"""
    c = st.session_state.db_conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (id,))
    st.session_state.db_conn.commit()

def add_staff(name, role, email, phone):
    """Add new staff member to database"""
    c = st.session_state.db_conn.cursor()
    c.execute("INSERT INTO staff (name, role, email, phone) VALUES (?, ?, ?, ?)",
              (name, role, email, phone))
    st.session_state.db_conn.commit()

def delete_staff(id):
    """Delete staff member from database"""
    c = st.session_state.db_conn.cursor()
    c.execute("DELETE FROM staff WHERE id=?", (id,))
    st.session_state.db_conn.commit()

def add_customer(name, email, phone):
    """Add new customer to database"""
    c = st.session_state.db_conn.cursor()
    c.execute("INSERT INTO customers (name, email, phone, total_purchases) VALUES (?, ?, ?, 0)",
              (name, email, phone))
    st.session_state.db_conn.commit()

def delete_customer(id):
    """Delete customer from database"""
    c = st.session_state.db_conn.cursor()
    c.execute("DELETE FROM customers WHERE id=?", (id,))
    st.session_state.db_conn.commit()

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 📦 Stationery Haven")
    st.markdown("<p>Management Dashboard</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "📦 Products", "👥 Staff", "👤 Customers", "📊 Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown('<div class="branding-footer">Crafted by Aarna</div>', unsafe_allow_html=True)

# ====================================
# 🏠 DASHBOARD PAGE
# ====================================
if page == "🏠 Dashboard":
    st.title("Dashboard Overview")
    
    # Get data
    products_df = get_products()
    staff_df = get_staff()
    customers_df = get_customers()
    
    # Calculate metrics
    total_stock = products_df['stock'].sum()
    store_value = (products_df['stock'] * products_df['price']).sum()
    
    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); color: white;">
                <h3 style="color: #e3f2fd;">📦 Total Stock</h3>
                <h1 style="color: white;">{total_stock}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #42a5f5 0%, #2196f3 100%); color: white;">
                <h3 style="color: #e3f2fd;">💰 Store Value</h3>
                <h1 style="color: white;">₹{store_value:,.0f}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%); color: white;">
                <h3 style="color: #e3f2fd;">👥 Staff Count</h3>
                <h1 style="color: white;">{len(staff_df)}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #90caf9 0%, #64b5f6 100%); color: white;">
                <h3 style="color: #e3f2fd;">👤 Customers</h3>
                <h1 style="color: white;">{len(customers_df)}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.subheader("Stock Distribution")
        fig = px.bar(products_df, x='name', y='stock', 
                     color_discrete_sequence=['#1976d2'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Product",
            yaxis_title="Stock Quantity",
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.subheader("Category Share")
        category_data = products_df.groupby('category')['stock'].sum().reset_index()
        fig = px.pie(category_data, values='stock', names='category',
                     color_discrete_sequence=['#0d47a1', '#1565c0', '#1976d2', '#1e88e5', '#42a5f5', '#64b5f6'])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            height=350
        )
        fig.update_traces(textposition='inside', textinfo='label+percent')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart Row 2
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.subheader("Price Trend")
    fig = px.line(products_df, x='name', y='price', markers=True,
                  color_discrete_sequence=['#1976d2'])
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Product",
        yaxis_title="Price (₹)",
        showlegend=False,
        height=350
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=10))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="branding-footer">Crafted by Aarna</div>', unsafe_allow_html=True)

# ====================================
# 📦 PRODUCTS PAGE
# ====================================
elif page == "📦 Products":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Products Inventory")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Product", type="primary", use_container_width=True):
            st.session_state.show_add_form = True
    
    # Add Product Form
    if st.session_state.get('show_add_form', False):
        with st.form("add_product_form", clear_on_submit=True):
            st.subheader("Add New Product")
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Product Name*")
                category = st.text_input("Category*")
            with col2:
                stock = st.number_input("Stock*", min_value=0, value=0, step=1)
                price = st.number_input("Price (₹)*", min_value=0.0, value=0.0, step=1.0)
            with col3:
                supplier = st.text_input("Supplier*")
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.form_submit_button("💾 Save", type="primary"):
                    if name and category and supplier:
                        add_product(name, category, stock, price, supplier)
                        st.session_state.show_add_form = False
                        st.success("✅ Product added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields!")
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_add_form = False
                    st.rerun()
    
    # Display Products Table
    products_df = get_products()
    
    if len(products_df) > 0:
        # Create a beautiful table display
        st.markdown("### 📋 Product List")
        
        # Table header
        header_cols = st.columns([2, 1.5, 1, 1, 1.5, 1.5])
        with header_cols[0]:
            st.markdown("**Product**")
        with header_cols[1]:
            st.markdown("**Category**")
        with header_cols[2]:
            st.markdown("**Stock**")
        with header_cols[3]:
            st.markdown("**Price**")
        with header_cols[4]:
            st.markdown("**Supplier**")
        with header_cols[5]:
            st.markdown("**Actions**")
        
        st.markdown("---")
        
        # Table rows
        for idx, row in products_df.iterrows():
            with st.expander(f"📦 {row['name']} | Stock: {row['stock']} | ₹{row['price']}"):
                with st.form(f"edit_form_{row['id']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        edit_name = st.text_input("Name", value=row['name'], key=f"name_{row['id']}")
                        edit_category = st.text_input("Category", value=row['category'], key=f"cat_{row['id']}")
                    with col2:
                        edit_stock = st.number_input("Stock", value=int(row['stock']), key=f"stock_{row['id']}")
                        edit_price = st.number_input("Price", value=float(row['price']), key=f"price_{row['id']}")
                    with col3:
                        edit_supplier = st.text_input("Supplier", value=row['supplier'], key=f"sup_{row['id']}")
                    
                    col1, col2, col3 = st.columns([1, 1, 4])
                    with col1:
                        if st.form_submit_button("✏️ Update", type="primary"):
                            update_product(row['id'], edit_name, edit_category, edit_stock, edit_price, edit_supplier)
                            st.success("✅ Product updated!")
                            st.rerun()
                    with col2:
                        if st.form_submit_button("🗑️ Delete", type="secondary"):
                            delete_product(row['id'])
                            st.success("✅ Product deleted!")
                            st.rerun()
    else:
        st.info("No products found. Add your first product!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    if len(products_df) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="plot-container">', unsafe_allow_html=True)
            st.subheader("Stock by Product")
            fig = px.bar(products_df, x='name', y='stock', color_discrete_sequence=['#42a5f5'])
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="plot-container">', unsafe_allow_html=True)
            st.subheader("Category Distribution")
            category_data = products_df.groupby('category')['stock'].sum().reset_index()
            fig = px.pie(category_data, values='stock', names='category',
                         color_discrete_sequence=['#0d47a1', '#1565c0', '#1976d2', '#1e88e5'])
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=350)
            fig.update_traces(textposition='inside', textinfo='label+percent')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="branding-footer">Crafted by Aarna</div>', unsafe_allow_html=True)

# ====================================
# 👥 STAFF PAGE
# ====================================
elif page == "👥 Staff":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Staff Management")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Staff", type="primary", use_container_width=True):
            st.session_state.show_add_staff = True
    
    # Add Staff Form
    if st.session_state.get('show_add_staff', False):
        with st.form("add_staff_form", clear_on_submit=True):
            st.subheader("Add New Staff Member")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*")
                role = st.text_input("Role*")
            with col2:
                email = st.text_input("Email*")
                phone = st.text_input("Phone*")
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.form_submit_button("💾 Save", type="primary"):
                    if name and role and email and phone:
                        add_staff(name, role, email, phone)
                        st.session_state.show_add_staff = False
                        st.success("✅ Staff member added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields!")
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_add_staff = False
                    st.rerun()
    
    # Display Staff
    staff_df = get_staff()
    
    if len(staff_df) > 0:
        col1, col2 = st.columns(2)
        
        for idx, row in staff_df.iterrows():
            with col1 if idx % 2 == 0 else col2:
                st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%);">
                        <h3 style="color: #0d47a1; margin-bottom: 10px;">👤 {row['name']}</h3>
                        <p style="color: #1565c0; font-weight: 600; margin: 5px 0; font-size: 16px;">{row['role']}</p>
                        <p style="color: #555; margin: 5px 0;">📧 {row['email']}</p>
                        <p style="color: #555; margin: 5px 0;">📱 {row['phone']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"🗑️ Remove", key=f"del_staff_{row['id']}", type="secondary", use_container_width=True):
                    delete_staff(row['id'])
                    st.success("✅ Staff member removed!")
                    st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("No staff members found. Add your first staff member!")
    
    st.markdown('<div class="branding-footer">Crafted by Aarna</div>', unsafe_allow_html=True)

# ====================================
# 👤 CUSTOMERS PAGE
# ====================================
elif page == "👤 Customers":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("Customer Management")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add Customer", type="primary", use_container_width=True):
            st.session_state.show_add_customer = True
    
    # Add Customer Form
    if st.session_state.get('show_add_customer', False):
        with st.form("add_customer_form", clear_on_submit=True):
            st.subheader("Add New Customer")
            col1, col2, col3 = st.columns(3)
            with col1:
                name = st.text_input("Full Name*")
            with col2:
                email = st.text_input("Email*")
            with col3:
                phone = st.text_input("Phone*")
            
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.form_submit_button("💾 Save", type="primary"):
                    if name and email and phone:
                        add_customer(name, email, phone)
                        st.session_state.show_add_customer = False
                        st.success("✅ Customer added successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields!")
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_add_customer = False
                    st.rerun()
    
    # Display Customers Table
    customers_df = get_customers()
    
    if len(customers_df) > 0:
        st.markdown("### 📋 Customer List")
        
        # Table header
        header_cols = st.columns([3, 3, 2, 2, 1])
        with header_cols[0]:
            st.markdown("**Name**")
        with header_cols[1]:
            st.markdown("**Email**")
        with header_cols[2]:
            st.markdown("**Phone**")
        with header_cols[3]:
            st.markdown("**Total Purchases**")
        with header_cols[4]:
            st.markdown("**Action**")
        
        st.markdown("---")
        
        # Table rows
        for idx, row in customers_df.iterrows():
            cols = st.columns([3, 3, 2, 2, 1])
            with cols[0]:
                st.write(f"**{row['name']}**")
            with cols[1]:
                st.write(row['email'])
            with cols[2]:
                st.write(row['phone'])
            with cols[3]:
                st.write(f"₹{row['total_purchases']:,.0f}")
            with cols[4]:
                if st.button("🗑️", key=f"del_cust_{row['id']}", type="secondary"):
                    delete_customer(row['id'])
                    st.success("✅ Customer removed!")
                    st.rerun()
            st.markdown("---")
    else:
        st.info("No customers found. Add your first customer!")
    
    st.markdown('<div class="branding-footer">Crafted by Aarna</div>', unsafe_allow_html=True)

# ====================================
# 📊 ANALYTICS PAGE
# ====================================
elif page == "📊 Analytics":
    st.title("Analytics & Insights")
    
    products_df = get_products()
    customers_df = get_customers()
    staff_df = get_staff()
    
    # Summary Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_value = (products_df['stock'] * products_df['price']).sum()
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); color: white;">
                <h3 style="color: #e3f2fd;">💰 Total Inventory Value</h3>
                <h1 style="color: white;">₹{total_value:,.0f}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_price = products_df['price'].mean()
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #42a5f5 0%, #2196f3 100%); color: white;">
                <h3 style="color: #e3f2fd;">📊 Average Price</h3>
                <h1 style="color: white;">₹{avg_price:.2f}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        customer_value = customers_df['total_purchases'].sum()
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%); color: white;">
                <h3 style="color: #e3f2fd;">👥 Customer Revenue</h3>
                <h1 style="color: white;">₹{customer_value:,.0f}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analytics Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.subheader("Top Products by Value")
        products_df['total_value'] = products_df['stock'] * products_df['price']
        top_products = products_df.nlargest(5, 'total_value')
        fig = px.bar(top_products, x='name', y='total_value',
                     color_discrete_sequence=['#1976d2'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Product",
            yaxis_title="Total Value (₹)",
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.subheader("Top Customers")
        top_customers = customers_df.nlargest(5, 'total_purchases')
        fig = px.bar(top_customers, x='name', y='total_purchases',
                     color_discrete_sequence=['#42a5f5'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Customer",
            yaxis_title="Total Purchases (₹)",
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analytics Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.subheader("Stock Value by Category")
        category_value = products_df.groupby('category').apply(
            lambda x: (x['stock'] * x['price']).sum()
        ).reset_index(name='value')
        fig = px.pie(category_value, values='value', names='category',
                     color_discrete_sequence=['#0d47a1', '#1565c0', '#1976d2', '#1e88e5', '#42a5f5', '#64b5f6'])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            height=350
        )
        fig.update_traces(textposition='inside', textinfo='label+percent')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="plot-container">', unsafe_allow_html=True)
        st.subheader("Price Range Distribution")
        fig = px.histogram(products_df, x='price', nbins=10,
                          color_discrete_sequence=['#42a5f5'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Price (₹)",
            yaxis_title="Count",
            showlegend=False,
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Analytics Insights
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.subheader("📈 Key Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        low_stock = products_df[products_df['stock'] < 100]
        st.markdown(f"""
            <div style="padding: 15px; background: #e3f2fd; border-radius: 10px; border-left: 4px solid #1976d2;">
                <h4 style="margin: 0; color: #0d47a1;">⚠️ Low Stock Alert</h4>
                <p style="margin: 5px 0; color: #555;">{len(low_stock)} products below 100 units</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_value = products_df[products_df['price'] > 100]
        st.markdown(f"""
            <div style="padding: 15px; background: #bbdefb; border-radius: 10px; border-left: 4px solid #1565c0;">
                <h4 style="margin: 0; color: #0d47a1;">💎 Premium Products</h4>
                <p style="margin: 5px 0; color: #555;">{len(high_value)} products above ₹100</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_customer_spend = customers_df['total_purchases'].mean()
        st.markdown(f"""
            <div style="padding: 15px; background: #90caf9; border-radius: 10px; border-left: 4px solid #1e88e5;">
                <h4 style="margin: 0; color: #0d47a1;">👤 Avg Customer Spend</h4>
                <p style="margin: 5px 0; color: #555;">₹{avg_customer_spend:,.2f} per customer</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="branding-footer">Crafted by Aarna</div>', unsafe_allow_html=True)