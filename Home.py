import streamlit as st
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, inspect
from sqlalchemy.exc import SQLAlchemyError

# Define database name and connection string.
DB_NAME = "bead_project.db"
CONNECTION_STRING = f"sqlite:///{DB_NAME}"

# ---------- Database Engine Setup with Caching ----------
@st.cache_resource(ttl=3600)
def get_engine():
    """
    Creates and returns an SQLAlchemy engine for the SQLite database.
    Caching prevents redundant initialization of the database engine.
    """
    return create_engine(CONNECTION_STRING)

engine = get_engine()
# Create an inspector instance to inspect the database schema.
inspector = inspect(engine)

# ---------- Utility Function: Create Table if Not Exists ----------
def create_table_if_not_exists(table_name, table_schema):
    """
    Uses SQLAlchemy metadata to create a table if it does not already exist.
    
    Parameters:
        table_name (str): The name of the table to create.
        table_schema (Table): The SQLAlchemy Table object defining the schema.
    """
    metadata = MetaData()
    table_schema.metadata = metadata
    metadata.create_all(engine)

# ---------- Contact Form Dialog ----------
@st.dialog("contact me")
def show_contact_form():
    """
    Displays a contact form dialog for users to submit feedback.
    This function validates user input and inserts the submitted data
    into the 'contact' table in the SQLite database.
    """
    # Collect user inputs.
    firstname = st.text_input("First name", key="contact_firstname")
    lastname = st.text_input("Last name", key="contact_lastname")
    email = st.text_input("Email", key="contact_email")
    message = st.text_area("Message for possible improvements", key="contact_message")
    submit_button = st.button("Submit", key="contact_submit")

    if submit_button:
        if firstname and lastname and email and message:
            try:
                with engine.begin() as connection:
                    # Define the 'contact' table schema.
                    contact_table = Table(
                        'contact', MetaData(),
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('firstname', String(255)),
                        Column('lastname', String(255)),
                        Column('email', String(255)),
                        Column('message', String(255))
                    )
                    # Create the table if it does not exist.
                    create_table_if_not_exists('contact', contact_table)
                    
                    # Insert user data with a parameterized query.
                    insert_query = contact_table.insert().values(
                        firstname=firstname,
                        lastname=lastname,
                        email=email,
                        message=message
                    )
                    connection.execute(insert_query)
            except SQLAlchemyError as e:
                st.error(f"An error occurred: {str(e)}")
            else:
                st.success("Thank you for your message! I will get back to you soon.")
        else:
            st.error("Please fill in all fields.")

# ---------- Sign Up Functionality ----------
def sign_up():
    """
    Renders a sign-up form for new users, validates inputs, stores user
    credentials securely in session state, and inserts the profile into
    the database. Redirects to another page on successful sign up.
    
    Returns:
        dict: A dictionary containing the user's email and password.
    """
    st.subheader("Sign Up")
    # Collect sign-up details.
    firstname = st.text_input("First Name", key="signup_firstname")
    lastname = st.text_input("Last Name", key="signup_lastname")
    email = st.text_input("Email", key="signup_email")
    create_password = st.text_input("Create Password", key="signup_create_password", type="password")
    confirm_password = st.text_input("Password", key="signup_confirm_password", type="password")
    submit_button = st.button("Submit", key="signup_submit")
    
    if submit_button:
        # Validate that all fields are completed.
        if firstname and lastname and email and create_password and confirm_password:
            if create_password == confirm_password:
                try:
                    with engine.begin() as connection:
                        # Define the 'profile' table schema.
                        profile_table = Table(
                            'profile', MetaData(),
                            Column('id', Integer, primary_key=True, autoincrement=True),
                            Column('firstname', String(255)),
                            Column('lastname', String(255)),
                            Column('email', String(255)),
                            Column('password', String(255))
                        )
                        # Create the table if it does not exist.
                        create_table_if_not_exists('profile', profile_table)
                        
                        # Insert user profile data.
                        insert_query = profile_table.insert().values(
                            firstname=firstname,
                            lastname=lastname,
                            email=email,
                            password=create_password  # Consider encrypting the password.
                        )
                        connection.execute(insert_query)
                except SQLAlchemyError as e:
                    st.error(f"An error occurred: {str(e)}")
                else:
                    # Save user credentials into session state.
                    st.session_state["EMAIL"] = email
                    st.session_state["PASSWORD"] = create_password
                    st.success("Account Created")
                    # Switch page after successful sign-up.
                    st.switch_page(r"main\pages\BeadPatternGeneraton.py")
            else:
                st.error("Passwords do not match.")
        else:
            st.error("Please fill in all fields.")
    
    # Return user data from session state if available.
    return {
        "email": st.session_state.get("EMAIL"),
        "password": st.session_state.get("PASSWORD")
    }

# ---------- Main Layout Setup ----------
def main():
    """
    Sets up the main layout of the web application, including columns for
    images and forms. Integrates the sign-up functionality and displays the
    contact dialog trigger.
    """
    # Define layout columns.
    col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
    
    with col1:
        st.image(
            r"main\logo\ChatGPT Image Apr 12, 2025, 12_25_09 AM.png",
            width=200
        )
    
    with col2:
        st.title("Welcome to Beader!")
        sign_up_data = sign_up()
        
    
    # Trigger the contact form dialog via a button.
    if st.button("Contact Us"):
        show_contact_form()

# ---------- Execute the Application ----------
if __name__ == "__main__":
    main()
