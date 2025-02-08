import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "http://api.nessieisreal.com"

CUSTOMER_ID = "67a7aa2f9683f20dd518bc17"
ACCOUNT_ID = "67a7aa2f9683f20dd518bc18"

def fetch_data(endpoint):
    url = f"{BASE_URL}{endpoint}?key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"🚨 조회 실패 ({endpoint}):", response.status_code, response.text)
        return None

def get_customer_info():
    print("\n📌 고객 정보 조회")
    customer_info = fetch_data(f"/customers/{CUSTOMER_ID}")
    print(json.dumps(customer_info, indent=4))

def get_account_info():
    print("\n📌 계좌 정보 조회")
    account_info = fetch_data(f"/accounts/{ACCOUNT_ID}")
    print(json.dumps(account_info, indent=4))

def get_loans():
    print("\n📌 대출 목록 조회")
    loans = fetch_data(f"/accounts/{ACCOUNT_ID}/loans")
    print(json.dumps(loans, indent=4))

def get_bills():
    print("\n📌 청구서 목록 조회")
    bills = fetch_data(f"/accounts/{ACCOUNT_ID}/bills")
    print(json.dumps(bills, indent=4))

if __name__ == "__main__":
    # get_customer_info()
    # get_account_info()
    # get_loans()
    get_bills()