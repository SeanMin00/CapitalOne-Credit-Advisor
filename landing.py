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

CUSTOMER_ID = ["67a7aa2f9683f20dd518bc17", "67a7e5fb9683f20dd518bdea"]



# ✅ Check Credentials (Replace with secure authentication)
def check_credentials(username, password):
    return username in CUSTOMER_ID and password == "p"


# ✅ Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# 🔹 Login Form
if not st.session_state["logged_in"]:
    st.image("logo.svg", width=800)
    st.title("Login")

    username = st.text_input("Capital One ID")
    password = st.text_input("Password", type="password", value = "p")
    aiText = "Optional: You can enable the Financial Advisor Chatbot with your OpenAI API Key"
    openAIKey = st.text_input("OpenAI API Key", placeholder = aiText)

    if st.button("Login"):
        if check_credentials(username, password):
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")

            # Store IDs in session state
            st.session_state["customer_id"] = username
            if openAIKey:
                st.session_state["openAI_key"] = openAIKey
                
            st.rerun() 
        else:
            st.error("Invalid username or password")

# Load Dashboard after login
if st.session_state.get("logged_in"):
    with open("test.py", encoding="utf-8") as f:
        code = f.read()
        exec(code)