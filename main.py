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

def run_flow(message: str) -> dict:
    """Send request to Langflow API and return the response."""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    payload = {"input_value": message, "output_type": "chat", "input_type": "chat", "tweaks": TWEAKS}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Streamlit UI
st.title("Langflow AI Agent")
user_input = st.text_area("Enter your message:")
if st.button("Submit"):
    if user_input.strip():
        response = run_flow(user_input)
        output = response.get("output_value", "No valid response received.")
        st.write("### Response:")
        st.write(output)
    else:
        st.warning("Please enter a message.")
