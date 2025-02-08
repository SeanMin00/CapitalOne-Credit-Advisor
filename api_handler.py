import requests
import os
from dotenv import load_dotenv

# 🔹 환경 변수 로드
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.nessieisreal.com"
HEADERS = {"Content-Type": "application/json"}

# ✅ 고객 생성 (Customer)
def create_customer():
    url = f"{BASE_URL}/customers?key={API_KEY}"
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "address": {
            "street_number": "123",
            "street_name": "Main Street",
            "city": "New York",
            "state": "NY",
            "zip": "10001"
        }
    }
    response = requests.post(url, headers=HEADERS, json=customer_data)
    if response.status_code == 201:
        return response.json()["objectCreated"]["_id"]
    return None

# ✅ 계좌 생성 (Account)
def create_account(customer_id):
    url = f"{BASE_URL}/customers/{customer_id}/accounts?key={API_KEY}"
    account_data = {
        "type": "Checking",
        "nickname": "John's Account",
        "rewards": 100,
        "balance": 10000
    }
    response = requests.post(url, headers=HEADERS, json=account_data)
    if response.status_code == 201:
        return response.json()["objectCreated"]["_id"]
    return None

# ✅ 대출 추가 (Loan)
def post_loans(account_id):
    url = f"{BASE_URL}/accounts/{account_id}/loans?key={API_KEY}"
    loans = [
        {"type": "home", "status": "pending", "credit_score": 750, "monthly_payment": 1200, "amount": 250000, "description": "Mortgage loan"},
        {"type": "auto", "status": "approved", "credit_score": 680, "monthly_payment": 350, "amount": 20000, "description": "Car loan"},
    ]
    results = []
    for loan in loans:
        response = requests.post(url, headers=HEADERS, json=loan)
        results.append(response.json())
    return results

# ✅ 대출 데이터 조회
def fetch_loans(account_id):
    url = f"{BASE_URL}/accounts/{account_id}/loans?key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []

# ✅ 계좌 잔액 조회
def fetch_balance(account_id):
    url = f"{BASE_URL}/accounts/{account_id}?key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["balance"]
    return 0