import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import openai
from loan_assistant import generate_loan_summary 


# 📌 Load API Key
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.nessieisreal.com"
HEADERS = {"Content-Type": "application/json"}

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
# ✅ Calculate Loan Amortization (Fixed)
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

        if principal_paid <= 0:  # Monthly payment too low
            st.error(f"⚠️ Monthly payment for {loan['type']} is too low! Increase payment or reduce interest rate.")
            break

        if balance < principal_paid:  # Adjust last payment
            principal_paid = balance
            interest_paid = 0  # No interest on final payment
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

        date += timedelta(days=30)  # Move to next month

    return schedule
# 🔹 UI: Title
st.title("📊 Loan Visualization Dashboard")

# ✅ Fetch account ID from session
account_id = st.session_state.get("account_id")

if account_id:
    # Fetch account balance
    balance = fetch_balance(account_id)
    
    # Fetch loans
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
    total_monthly_payment = 0
    for loan in loans:
        if loan["_id"] in interest_rates:
            schedule = calculate_amortization(loan, interest_rates[loan["_id"]])
            payoff_schedules.extend(schedule)
            total_monthly_payment += loan["monthly_payment"]

    df_schedule = pd.DataFrame(payoff_schedules)
    total_loan_amount = sum(loan["amount"] for loan in loans)

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
        balance_color = "green" if balance >= total_monthly_payment else "red"
        st.markdown(f"### 💵 Account Balance: <span style='color:{balance_color}; font-weight:bold;'>${balance:,}</span>", unsafe_allow_html=True)

        st.metric("⏳ Time Until Debt-Free", f"{months_left} months" if months_left != "N/A" else "N/A")

    # 📊 Loan Breakdown Pie Chart
    df_loans = pd.DataFrame(loans)
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

    # ✅ Compute Loan Stats
    total_loan = sum(loan["amount"] for loan in loans)
    balance = 10000  # Placeholder balance

    # ✅ Find the fastest-finishing loan
    def get_fastest_loan(loans):
        if not loans:
            return "No loans available"
        loans_sorted = sorted(loans, key=lambda x: x["monthly_payment"] / x["amount"] if x["amount"] > 0 else float("inf"))
        return f"{loans_sorted[0]['type']} loan (fastest to be paid off)"

    fastest_loan_info = get_fastest_loan(loans)

    # ✅ Capital One Loan Products Reference
    capitalone_products = (
        "Capital One Loan Products:\n"
        "- **Product A**: Low interest rate, 36-month repayment.\n"
        "- **Product B**: Flexible repayment options, credit improvement support.\n"
        "- **Product C**: Fast approval, short-term loan."
    )

    # -------------------------------
    # 🔹 Display Loan Summary with Streaming
    # -------------------------------
    st.subheader("🔹 Loan Summary")

    with st.spinner("Generating loan summary..."):
        streamed_text = ""
        summary_container = st.empty()

        for chunk in generate_loan_summary(total_loan, balance, fastest_loan_info, capitalone_products):
            text_chunk = chunk.strip()  # Remove leading/trailing spaces
            if not streamed_text.endswith(" "):  # Ensure spaces between chunks
                streamed_text += " "
            streamed_text += text_chunk
            summary_container.markdown(f"**{streamed_text}**", unsafe_allow_html=True)



    # ✅ Compute Loan Stats
    total_loan = sum(loan["amount"] for loan in loans)
    balance = 10000  # Placeholder balance

    # ✅ Find the fastest-finishing loan
    def get_fastest_loan(loans):
        if not loans:
            return "No loans available"
        loans_sorted = sorted(loans, key=lambda x: x["monthly_payment"] / x["amount"] if x["amount"] > 0 else float("inf"))
        return f"{loans_sorted[0]['type']} loan (fastest to be paid off)"

    fastest_loan_info = get_fastest_loan(loans)

    # ✅ Capital One Loan Products Reference
    capitalone_products = (
        "Capital One Loan Products:\n"
        "- **Product A**: Low interest rate, 36-month repayment.\n"
        "- **Product B**: Flexible repayment options, credit improvement support.\n"
        "- **Product C**: Fast approval, short-term loan."
    )

    # -------------------------------
    # 🔹 Display Loan Summary with Streaming
    # -------------------------------
    st.subheader("🔹 Loan Summary")

    with st.spinner("Generating loan summary..."):
        streamed_text = ""
        summary_container = st.empty()

        for chunk in generate_loan_summary(total_loan, balance, fastest_loan_info, capitalone_products):
            text_chunk = chunk.strip()  # Remove leading/trailing spaces
            if not streamed_text.endswith(" "):  # Ensure spaces between chunks
                streamed_text += " "
            streamed_text += text_chunk
            summary_container.markdown(f"**{streamed_text}**", unsafe_allow_html=True)



else:
    st.warning("⚠️ Please log in first!")