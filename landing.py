import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# 📌 Load API Key
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.nessieisreal.com"
HEADERS = {"Content-Type": "application/json"}

# ✅ Fetch Customer Account ID
def fetch_account_id(customer_id):
    url = f"{BASE_URL}/customers/{customer_id}/accounts?key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200 and response.json():
        return response.json()[0]["_id"]  # Get first account ID
    return None

# ✅ Check Credentials (Replace with secure authentication)
def check_credentials(username, password):
    return username == "u" and password == "p"

# ✅ Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 🔹 Login Form
if not st.session_state["logged_in"]:
    st.image("logo.svg", width=800)
    st.title("Login")

    username = st.text_input("Capital One ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_credentials(username, password):
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")

            # Fetch the Account ID dynamically
            CUSTOMER_ID = "67a7aa2f9683f20dd518bc17"  # Predefined for now
            account_id = fetch_account_id(CUSTOMER_ID)

            if account_id:
                st.session_state["account_id"] = account_id
                st.rerun()  # Reload to transition to dashboard
            else:
                st.error("Could not fetch account ID. Contact support.")
        else:
            st.error("Invalid username or password")

# ✅ Load Dashboard after login
if st.session_state.get("logged_in") and "account_id" in st.session_state:
    with open("test.py", encoding="utf-8") as f:
        code = f.read()
        exec(code)