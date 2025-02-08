import openai
import streamlit as st
import os

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the client
client = openai.Client(api_key=openai.api_key)


completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)



print(completion.choices[0].message)
print("hello")

@st.cache_data
def create_assistant():
    client = openai.OpenAI()
    assistant = client.beta.assistants.create(
        name="Financial Loan Advisor",
        instructions=(
            "You are a financial assistant specialized in analyzing loans. "
            "Summarize the user's loan status in three bullet points:\n"
            "1. A one-line comment on their financial situation.\n"
            "2. Compare the account balance and total loan amount.\n"
            "3. Identify the loan that finishes first and recommend a suitable Capital One loan product.\n"
        ),
        tools=[],  # Add tools like `code_interpreter` if needed
        model="gpt-4o",
    )
    return assistant.id

assistant_id = create_assistant()

@st.cache_data
def create_thread():
    client = openai.OpenAI()
    thread = client.beta.threads.create()
    return thread.id

thread_id = create_thread()

def add_message_to_thread(thread_id, user_input):
    client = openai.OpenAI()
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

def run_assistant(thread_id, assistant_id):
    client = openai.OpenAI()
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    
    # Get the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content

# Streamlit App UI
st.title("📊 Loan Assistant with OpenAI's Assistants API")

# User input for loan details
user_query = st.text_area("Enter your loan details or ask a financial question:")

if st.button("Get Loan Summary"):
    if user_query:
        add_message_to_thread(thread_id, user_query)
        response = run_assistant(thread_id, assistant_id)
        st.subheader("🔹 Assistant Summary:")
        st.markdown(response)
    else:
        st.warning("Please enter loan details or a question.")
