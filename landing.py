import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# 📌 Load API Key
load_dotenv()
API_KEY = "ad96e72d43ad9c0a3e39125921b15882"
BASE_URL = "http://api.nessieisreal.com"
HEADERS = {"Content-Type": "application/json"}
CUSTOMER_ID = ["67a8b7d59683f20dd518bea4", "67a8b7d59683f20dd518bea8","67a8b7d49683f20dd518bea0", "67a84cb69683f20dd518be90", "67a7e5fb9683f20dd518bdea"]

# Check Credentials (Replace with secure authentication)
def check_credentials(username, password):
    return username in CUSTOMER_ID and (len(password) > 6)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Login Form
if not st.session_state["logged_in"]:
    st.image("logo.svg", width=800)
    st.markdown(
        """
        <style>
        @font-face {
            font-family: 'FrutigerBlackItalic';
            src: url('FrutigerBlackItalic.ttf') format('truetype');
        }
        .centered-title {
            text-align: center;
            font-family: 'FrutigerBlackItalic';
            color: #FFFFFF;
        }
        </style>
        <div class="centered-title">
            <h1>Loan Advisor</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ✅ User selects ID from dropdown
    username = st.selectbox("Select Your Capital One ID", options=CUSTOMER_ID)

    password = st.text_input("Password", type="password", value = "********")
    aiText = "Financial Advisor Chatbot is available without OpenAI API Key only during the hackathon"
    openAIKey = st.text_input("OpenAI API Key", placeholder=aiText)

    if st.button("Sign in"):
        if check_credentials(username, password):
            st.session_state["logged_in"] = True
            st.success("Logged in successfully!")

            # Store IDs and OpenAI API key in session state
            st.session_state["customer_id"] = username
            if openAIKey:
                st.session_state["openAI_key"] = openAIKey
                
            # Reload to transition to the dashboard
            st.rerun() 
        else:
            st.error("Invalid username or password")

    # st.text("")
    
    # # 🔹 Display Available Customer IDs Below the Sign-In Button
    # st.markdown("##### Available Customer IDs to login (Password is same):")
    # for customer in CUSTOMER_ID:
    #     st.write(f"- `{customer}`")

    
    


def get_openAI_key():
    return openAIKey

# Load Dashboard after login
if st.session_state.get("logged_in"):

    openai_key = st.session_state.get("openAI_key")

    import loan_assistant
    
    with open("test.py", encoding="utf-8") as f:
        code = f.read()
        exec(code)

