import openai
import os
import streamlit as st
from dotenv import load_dotenv

# ✅ Load environment variables (API keys)
load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = st.session_state.get("openAI_key")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please set it in your .env file.")

# ✅ Initialize OpenAI Client
client = openai.Client(api_key=openai.api_key)

def generate_loan_summary(total_loan, balance, fastest_loan_info):
    """
    Generates a 3-bullet-point loan summary using OpenAI API (streaming).
    
    Args:
        total_loan (float): Total loan amount.
        balance (float): Account balance.
        fastest_loan_info (str): Information about the fastest-finishing loan.

    Returns:
        Generator[str]: Streaming response from OpenAI (chunked).
    """
    messages = [
        {"role": "system", "content": "You are a financial assistant specialized in loan analysis. Provide structured responses in bullet points."},
        {"role": "user", "content": f"""
Summarize the customer's loan status in 3 bullet points and add a empty line after each point:

1. Provide a one-line comment on their overall financial situation.
        
2. Compare the account balance with the total loan amount.
        
3. Suggest future plans in one sentence
Customer Data:
- **Total Loan Amount**: ${total_loan:,}
- **Account Balance**: ${balance:,}
- **Fastest Finishing Loan**: {fastest_loan_info}

"""}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True  # Enable streaming
    )

    for chunk in response:
        if chunk.choices[0].delta.content:  # Correct streaming syntax
            yield chunk.choices[0].delta.content  # Return response chunk-by-chunk