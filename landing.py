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
CUSTOMER_ID = ["67a7aa2f9683f20dd518bc17", "67a84cb69683f20dd518be90","56c66be5a73e492741507293","5e47855e322fa016762f38e2"]

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

    username = st.text_input("Capital One ID (customer_id)", value = CUSTOMER_ID[0])
    password = st.text_input("Password", type="password", value = "********")
    aiText = "Optional: You can enable the Financial Advisor Chatbot with your OpenAI API Key"
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

    
    
    # 🔹 Display Available Customer IDs Below the Sign-In Button
    st.markdown("##### Other Available Customer IDs to login (Password is all the same):")
    for customer in CUSTOMER_ID:
        st.write(f"- `{customer}`")

    
    


def get_openAI_key():
    return openAIKey

# Load Dashboard after login
if st.session_state.get("logged_in"):

    openai_key = st.session_state.get("openAI_key")

    import loan_assistant
    
    with open("test.py", encoding="utf-8") as f:
        code = f.read()
        exec(code)

