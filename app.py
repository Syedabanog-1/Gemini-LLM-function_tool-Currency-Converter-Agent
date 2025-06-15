import streamlit as st
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration
import os
import requests
from dotenv import load_dotenv

# ✅ Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Real-time currency conversion function
def convert_currency(from_currency: str, to_currency: str, amount: float) -> str:
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "rates" not in data:
        raise Exception("Failed to fetch exchange rate.")

    rate = data["rates"].get(to_currency.upper())
    if rate is None:
        return f"Currency '{to_currency}' not supported."

    converted = amount * rate
    return f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()} (Rate: {rate:.2f})"

# ✅ Define function for Gemini tool
conversion_function = FunctionDeclaration(
    name="convert_currency",
    description="Convert a specific amount from one currency to another using real-time exchange rate.",
    parameters={
        "type": "object",
        "properties": {
            "from_currency": {"type": "string", "description": "e.g., USD"},
            "to_currency": {"type": "string", "description": "e.g., PKR"},
            "amount": {"type": "number", "description": "Amount to convert"}
        },
        "required": ["from_currency", "to_currency", "amount"]
    }
)

# ✅ Load Gemini model with tool function
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[conversion_function],
    function_calling_config={"convert_currency": {"function": convert_currency}}
)

# ✅ Streamlit UI
st.title("💱 Currency Converter with Gemini")

query = st.text_input("Enter a conversion query (e.g., 'Convert 100 USD to PKR')")

if st.button("Get Response"):
    with st.spinner("Thinking..."):
        try:
            convo = model.start_chat()

            prompt = f"""
You are a currency conversion assistant. When the user says something like:
"Convert 50 USD to PKR" or "How much is 200 EUR in PKR",
→ Extract values and call `convert_currency`.

User's query:
{query}
"""

            response = convo.send_message(prompt)

            if hasattr(response, "text"):
                st.success("✅ Gemini says:")
                st.write(response.text)
            else:
                st.warning("⚠️ No valid response received.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
