import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 📌 Load API Key
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.nessieisreal.com"
HEADERS = {"Content-Type": "application/json"}

# ✅ Fetch Loans
def fetch_loans(account_id):
    url = f"{BASE_URL}/accounts/{account_id}/loans?key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

# ✅ Calculate Loan Amortization
def calculate_amortization(loan, interest_rate):
    balance = loan["amount"]
    monthly_payment = loan["monthly_payment"]
    rate = interest_rate / 12  # Monthly interest rate

    schedule = []
    date = datetime.today()

    while balance > 0:
        interest_paid = balance * rate
        principal_paid = monthly_payment - interest_paid
        balance -= principal_paid

        if balance < 0:  # Adjust last payment
            principal_paid += balance
            balance = 0

        schedule.append({
            "Date": date.strftime("%Y-%m"),
            "Loan Type": loan["type"],
            "Remaining Balance": balance,
            "Principal Paid": principal_paid,
            "Interest Paid": interest_paid,
        })

        date += timedelta(days=30)  # Move to next month

    return schedule

# 🔹 UI: Title
st.title("📊 Loan Visualization Dashboard")

# 🔹 Account ID Input
account_id = "67a7aa2f9683f20dd518bc18"

if account_id:
    loans = fetch_loans(account_id)

    # 🔹 User Adjustable Interest Rates
    interest_rates = {}
    with st.sidebar:
        st.header("Adjust Interest Rates")
        for loan in loans:
            interest_rates[loan["_id"]] = st.slider(
                f"{loan['type'].capitalize()} Loan Interest Rate (%)",
                min_value=0.0, max_value=20.0, value=5.0, step=0.1
            ) / 100  # Convert to decimal

    # 📌 Process Loans
    payoff_schedules = []
    for loan in loans:
        if loan["_id"] in interest_rates:
            schedule = calculate_amortization(loan, interest_rates[loan["_id"]])
            payoff_schedules.extend(schedule)

    df_schedule = pd.DataFrame(payoff_schedules)

    # 📊 Loan Payoff Timeline (Separate Graphs)
    st.subheader("📆 Loan Payoff Timeline")
    fig_timeline = px.line(
        df_schedule, x="Date", y="Remaining Balance",
        color="Loan Type",
        title="When Will Loans Be Fully Paid Off?",
        labels={"Date": "Month", "Remaining Balance": "Amount ($)"},
        markers=True,
        facet_row="Loan Type"  # Creates separate charts for each loan type
    )
    st.plotly_chart(fig_timeline)

    # 📊 Principal vs Interest Over Time (Separate Graphs)
    st.subheader("📊 Principal vs Interest Breakdown")
    fig_stack = px.area(
        df_schedule, x="Date", y=["Principal Paid", "Interest Paid"],
        facet_row="Loan Type",  # Creates separate plots
        title="How Loan Payments Change Over Time",
        labels={"value": "Amount ($)"}
    )
    st.plotly_chart(fig_stack)

    # 📋 Loan Details Table
    st.subheader("📋 Loan Details")
    st.dataframe(pd.DataFrame(loans)[["type", "amount", "monthly_payment", "credit_score", "status"]])

else:
    st.warning("Please enter your Account ID to fetch loan details!")