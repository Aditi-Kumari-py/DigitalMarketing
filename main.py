import streamlit as st
import requests
import json

# API Config
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "42bad0c1-2b9b-44cb-8c3f-ef88855f54ac"
FLOW_ID = "a631b2a9-63be-4f7d-99f2-b095b8735a9b"
APPLICATION_TOKEN = "AstraCS:lmqTcMopslHNxGkESPiQtByh:ddd6464f67cf59f425dec18e1c5a0260c6ad4cabd0dfa43db69ef2850353c17c"
ENDPOINT = FLOW_ID  # Default to flow ID
TWEAKS = {}

def run_flow(message: str) -> str:
    """Send request to Langflow API and return only the AI's response text."""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    payload = {"input_value": message, "output_type": "chat", "input_type": "chat", "tweaks": TWEAKS}

    response = requests.post(api_url, json=payload, headers=headers).json()

    # Extract only the AI's response text
    try:
        return response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except (KeyError, IndexError):
        return "Error: Unable to retrieve response. Please check API output."


# Streamlit UI
st.title("Digital Marketing Agent")
user_input = st.text_area("Enter your message:")
if st.button("Submit"):
    if user_input.strip():
        response_text = run_flow(user_input)
        st.write("### Response:")
        st.write(response_text)  # Show only AI's message
    else:
        st.warning("Please enter a message.")

