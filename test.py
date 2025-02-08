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

# ✅ Fetch Accounts for a Customer
def fetch_accounts(customer_id):
    url = f"{BASE_URL}/customers/{customer_id}/accounts?key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

# ✅ Fetch Account Balance
def fetch_balance(account_id):
    url = f"{BASE_URL}/accounts/{account_id}?key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    return response.json().get("balance", 0) if response.status_code == 200 else 0

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
    total_interest_paid = 0
    total_principal_paid = 0

    while balance > 0:
        interest_paid = balance * rate
        principal_paid = monthly_payment - interest_paid

        if principal_paid <= 0:
            st.error(f"⚠️ Monthly payment for {loan['type']} is too low! Increase payment or reduce interest rate.")
            break

        if balance < principal_paid:
            principal_paid = balance
            interest_paid = 0
            balance = 0
        else:
            balance -= principal_paid

        total_interest_paid += interest_paid
        total_principal_paid += principal_paid

        schedule.append({
            "Date": date.strftime("%Y-%m"),
            "Loan Type": loan["type"],
            "Remaining Balance": balance,
            "Principal Paid": principal_paid,
            "Interest Paid": interest_paid,
            "Total Principal Paid": total_principal_paid,
            "Total Interest Paid": total_interest_paid,
            "Principal %": (total_principal_paid / (total_principal_paid + total_interest_paid)) * 100 if (total_principal_paid + total_interest_paid) > 0 else 0,
            "Interest %": (total_interest_paid / (total_principal_paid + total_interest_paid)) * 100 if (total_principal_paid + total_interest_paid) > 0 else 0,
        })

        date += timedelta(days=30)

    return schedule

# 🔹 UI: Title
st.title("📊 Loan Visualization Dashboard")

# ✅ Fetch customer ID from session
customer_id = st.session_state.get("customer_id")

if customer_id:
    # Fetch all accounts linked to this customer
    accounts = fetch_accounts(customer_id)

    if not accounts:
        st.warning("⚠️ No accounts found for this customer.")
        st.stop()

    # Fetch balances and loans for all accounts
    total_balance = 0
    all_loans = []
    for account in accounts:
        total_balance += fetch_balance(account["_id"])
        all_loans.extend(fetch_loans(account["_id"]))

    # 🔹 User Adjustable Interest Rates
    interest_rates = {}
    with st.sidebar:
        st.header("Adjust Interest Rates")
        for loan in all_loans:
            interest_rates[loan["_id"]] = st.slider(
                f"{loan['type'].capitalize()} Loan Interest Rate (%)",
                min_value=0.0, max_value=20.0, value=5.0, step=0.1
            ) / 100  # Convert to decimal

    # 📌 Process Loans
    payoff_schedules = []
    total_monthly_payment = 0
    for loan in all_loans:
        if loan["_id"] in interest_rates:
            schedule = calculate_amortization(loan, interest_rates[loan["_id"]])
            payoff_schedules.extend(schedule)
            total_monthly_payment += loan["monthly_payment"]

    df_schedule = pd.DataFrame(payoff_schedules)
    total_loan_amount = sum(loan["amount"] for loan in all_loans)

    # 📌 Debt-Free Date Calculation
    latest_payment_date = df_schedule[df_schedule["Remaining Balance"] == 0]["Date"].max()
    debt_free_date = datetime.strptime(latest_payment_date, "%Y-%m") if latest_payment_date else None
    months_left = (debt_free_date - datetime.today()).days // 30 if debt_free_date else "N/A"

    # ✅ Sidebar Overview
    with st.sidebar:
        st.header("Loan Overview")
        st.metric("📦 Total Loan Amount", f"${total_loan_amount:,}")
        st.metric("📅 Monthly Payment", f"${total_monthly_payment:,}")
        
        # 🔹 Balance Warning / Success
        balance_color = "green" if total_balance >= total_monthly_payment else "red"
        st.markdown(f"### 💵 Total Account Balance: <span style='color:{balance_color}; font-weight:bold;'>${total_balance:,}</span>", unsafe_allow_html=True)

        st.metric("⏳ Time Until Debt-Free", f"{months_left} months" if months_left != "N/A" else "N/A")

    # 📊 Loan Breakdown Pie Chart
    df_loans = pd.DataFrame(all_loans)
    st.subheader("📊 Loan Breakdown by Type")
    if not df_loans.empty:
        fig_pie = px.pie(df_loans, names="type", values="amount", title="Loan Distribution")
        st.plotly_chart(fig_pie)
    else:
        st.warning("⚠️ No loan data available for pie chart.")

    # 📊 Principal vs. Interest Over Time
    st.subheader("📊 Monthly Payment Breakdown Over Time")
    if not df_schedule.empty:
        fig_breakdown = px.area(
            df_schedule, x="Date", y=["Principal %", "Interest %"],
            color_discrete_map={"Principal %": "orange", "Interest %": "green"},
            facet_row="Loan Type",
            title="How Monthly Payments Change Over Time",
            labels={"value": "Percentage (%)", "variable": "Payment Component"},
        )
        st.plotly_chart(fig_breakdown)
    else:
        st.warning("⚠️ No loan data available for payment breakdown.")

    # 📊 Loan Payoff Timeline
    st.subheader("📆 Loan Payoff Timeline")
    if not df_schedule.empty:
        fig_timeline = px.line(df_schedule, x="Date", y="Remaining Balance", color="Loan Type", markers=True, facet_row="Loan Type")
        st.plotly_chart(fig_timeline)
    else:
        st.warning("⚠️ No loan data available for timeline.")

    # 📋 Loan Details Table
    st.subheader("📋 Loan Details")
    st.dataframe(df_loans[["type", "amount", "monthly_payment", "credit_score", "status"]])

else:
    st.warning("⚠️ Please log in first!")