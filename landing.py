import streamlit as st
import pandas as pd
import math

CUSTOMER_ID = "67a7aa2f9683f20dd518bc17"

# Function to check credentials
def check_credentials(username, password):
    # Replace with your own logic to check credentials
    return username == "u" and password == "p"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Login form
if not st.session_state["logged_in"]:
    # Capital One Logo
    st.image("logo.svg", width=1000)

    # Login Section
    st.title("Login")
    username = st.text_input("Capital One ID")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_credentials(username, password):
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")
            
            # Clear login page
            st.rerun()
        else:
            st.error("Invalid username or password")
else:
    # Log In Successful   
    # Execute test.py to show the dashboard
    with open("test.py", encoding="utf-8") as f:
        code = f.read()
        exec(code)