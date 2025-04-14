import os
import tempfile
import hashlib
import streamlit as st
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# =============================================
# DATABASE SETUP WITH PROPER PATH HANDLING
# =============================================

def get_database_path():
    """Determine the appropriate database path based on environment"""
    if 'DB_PATH' in st.secrets:  # For custom configuration
        return st.secrets.DB_PATH
    elif os.getenv("IS_STREAMLIT_CLOUD"):  # Streamlit Cloud environment
        return os.path.join(tempfile.gettempdir(), "bead_app.db")
    else:  # Local development
        return "local_bead_app.db"

def initialize_database(engine):
    """Create all required tables with proper schema"""
    metadata = MetaData()
    
    # Profile table with security features
    Table(
        'profile', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('firstname', String(255), nullable=False),
        Column('lastname', String(255), nullable=False),
        Column('email', String(255), unique=True, nullable=False),
        Column('password_hash', String(255), nullable=False),
        Column('salt', String(255), nullable=False),
        Column('created_at', DateTime, default=datetime.utcnow),
        Column('last_login', DateTime),
        extend_existing=True
    )
    
    # Contact messages table
    Table(
        'contact', metadata,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('firstname', String(255)),
        Column('lastname', String(255)),
        Column('email', String(255)),
        Column('message', String(1000)),
        Column('submitted_at', DateTime, default=datetime.utcnow),
        extend_existing=True
    )
    
    metadata.create_all(engine)

@st.cache_resource(ttl=3600)
def get_database_engine():
    """Get a configured database engine with connection pooling"""
    db_path = get_database_path()
    connection_string = f"sqlite:///{db_path}"
    engine = create_engine(connection_string, pool_pre_ping=True)
    
    # Initialize tables if this is a new database
    if not os.path.exists(db_path):
        initialize_database(engine)
    
    return engine

# Initialize the database engine
engine = get_database_engine()

# =============================================
# SECURITY FUNCTIONS
# =============================================

def generate_salt():
    """Generate a random salt for password hashing"""
    return os.urandom(16).hex()

def hash_password(password, salt):
    """Hash password with salt using PBKDF2-HMAC-SHA256"""
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # Number of iterations
    ).hex()

# =============================================
# APPLICATION FUNCTIONS
# =============================================

def sign_up():
    """User registration with proper validation and security"""
    st.subheader("Sign Up")
    
    with st.form("signup_form"):
        firstname = st.text_input("First Name", max_chars=50)
        lastname = st.text_input("Last Name", max_chars=50)
        email = st.text_input("Email", max_chars=100).strip().lower()
        password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            # Validate inputs
            if not all([firstname, lastname, email, password, confirm_password]):
                st.error("Please fill in all fields")
                return
                
            if password != confirm_password:
                st.error("Passwords do not match")
                return
                
            if len(password) < 8:
                st.error("Password must be at least 8 characters")
                return
                
            # Secure password handling
            salt = generate_salt()
            password_hash = hash_password(password, salt)
            
            try:
                with engine.begin() as conn:
                    conn.execute(
                        """INSERT INTO profile 
                        (firstname, lastname, email, password_hash, salt) 
                        VALUES (?, ?, ?, ?, ?)""",
                        (firstname, lastname, email, password_hash, salt)
                    )
                    
                st.session_state.user_email = email
                st.success("Account created successfully!")
                st.balloons()
                time.sleep(2)
                st.switch_page("main_app.py")
                
            except SQLAlchemyError as e:
                if "UNIQUE constraint failed" in str(e):
                    st.error("This email is already registered")
                else:
                    st.error(f"Registration failed: {str(e)}")

@st.dialog("Contact Us")
def show_contact_form():
    """Contact form with proper validation"""
    with st.form("contact_form"):
        firstname = st.text_input("First name", max_chars=50)
        lastname = st.text_input("Last name", max_chars=50)
        email = st.text_input("Email", max_chars=100)
        message = st.text_area("Your message", max_chars=1000)
        submitted = st.form_submit_button("Send Message")
        
        if submitted:
            if not all([firstname, lastname, email, message]):
                st.error("Please fill in all fields")
                return
                
            try:
                with engine.begin() as conn:
                    conn.execute(
                        """INSERT INTO contact 
                        (firstname, lastname, email, message) 
                        VALUES (?, ?, ?, ?)""",
                        (firstname, lastname, email, message)
                    )
                st.success("Thank you for your message!")
                time.sleep(2)
                st.rerun()
            except SQLAlchemyError as e:
                st.error(f"Failed to send message: {str(e)}")

# =============================================
# MAIN APPLICATION LAYOUT
# =============================================

def main():
    """Main application layout"""
    st.set_page_config(page_title="Bead Pattern Generator", layout="wide")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("app_logo.png", width=200)
    
    with col2:
        st.title("Welcome to Bead Pattern Generator")
        sign_up()
    
    if st.button("Contact Support"):
        show_contact_form()

if __name__ == "__main__":
    main()
