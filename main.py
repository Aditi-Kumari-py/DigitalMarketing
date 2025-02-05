import json
import requests
import streamlit as st

st.set_page_config(page_title="Digital Marketing AI Agent")

# ✅ Define API variables
BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "42bad0c1-2b9b-44cb-8c3f-ef88855f54ac"
FLOW_ID = "a631b2a9-63be-4f7d-99f2-b095b8735a9b"
APPLICATION_TOKEN = "AstraCS:lmqTcMopslHNxGkESPiQtByh:ddd6464f67cf59f425dec18e1c5a0260c6ad4cabd0dfa43db69ef2850353c17c"
ENDPOINT = FLOW_ID  # Use FLOW_ID as default
TWEAKS = {}  # ✅ Ensure tweaks are defined

def run_flow(message: str) -> str:
    """Send request to Langflow API and return only the AI's response text."""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    
    # Modify the payload to avoid history storage and limit response length
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": TWEAKS,  # Ensures no unnecessary history is stored
        "max_tokens": 500  # Keeps responses within a safe range
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)

        # Debugging: Show API response for troubleshooting
        print("Full API Response:", response.text)

        # Handle HTTP errors
        if response.status_code != 200:
            return f"Error: API returned status {response.status_code} - {response.text}"

        # Convert to JSON
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            return "Error: API response is not valid JSON."

        # ✅ Extract only the AI’s message safely
        outputs = response_json.get("outputs", [])
        if outputs and "outputs" in outputs[0] and "results" in outputs[0]["outputs"][0]:
            return outputs[0]["outputs"][0]["results"]["message"]["text"]

        return "Error: Unexpected API response format."

    except requests.exceptions.RequestException as e:
        return f"Error: Request failed - {str(e)}"

# 🎨 Streamlit UI
st.title("Digital Marketing AI Agent")
user_input = st.text_area("Enter your message:")
if st.button("Submit"):
    if user_input.strip():
        response_text = run_flow(user_input)
        st.write("### Response:")
        st.write(response_text)  # Show only AI's message
    else:
        st.warning("Please enter a message.")
