import streamlit as st
import pandas as pd
import plotly.express as px
from api_handler import create_customer, create_account, post_loans, fetch_loans, fetch_balance

# 🔹 고객 및 계좌 생성 (초기 설정)
st.title("📊 Loan Visualization Dashboard")
if "customer_id" not in st.session_state:
    customer_id = create_customer()
    account_id = create_account(customer_id)
    st.session_state["customer_id"] = customer_id
    st.session_state["account_id"] = account_id
    post_loans(account_id)

account_id = st.session_state["account_id"]

# 🔹 데이터 가져오기
loans = fetch_loans(account_id)
balance = fetch_balance(account_id)

# 🔹 대출 데이터가 있을 경우 분석
if loans:
    df = pd.DataFrame(loans)

    # 📌 총 대출 금액
    total_loan = df["amount"].sum()

    # 📌 평균 이자율 (고정 이자율 5% 적용)
    interest_rate = 0.05  # 5% 가정

    # 📌 월 납입액
    total_monthly_payment = df["monthly_payment"].sum()

    # 📌 남은 개월 수 계산 (이자 포함)
    def calculate_remaining_months(amount, monthly_payment, rate):
        if monthly_payment == 0 or rate == 0:
            return "N/A"
        r = rate / 12  # 월 이자율
        months = (amount * r) / (monthly_payment - (amount * r))
        return round(months) if months > 0 else "N/A"

    remaining_months = calculate_remaining_months(total_loan, total_monthly_payment, interest_rate)

    # 🔹 왼쪽 상단 대출 개요
    with st.sidebar:
        st.header("Loan Overview")
        st.metric("📦 총 대출 금액", f"${total_loan:,}")
        st.metric("📅 월 납입액", f"${total_monthly_payment:,}")
        st.metric("💰 이자율 (가정)", f"{interest_rate * 100:.2f}%")
        st.metric("⏳ 남은 개월 수", f"{remaining_months} months")

        st.header("Account Balance")
        st.metric("💵 현재 계좌 잔액", f"${balance:,}")
        st.metric("📆 이번 달 예상 납입액", f"${total_monthly_payment:,}")

    # 🔹 대출 유형별 파이 차트
    fig = px.pie(df, names="type", values="amount", title="Loan Breakdown by Type")
    st.plotly_chart(fig)

    # 🔹 대출 상세 테이블
    st.header("📋 Loan Details")
    st.dataframe(df[["type", "amount", "monthly_payment", "credit_score", "status"]])

else:
    st.warning("⚠️ No loan data available!")