import streamlit as st
import google.generativeai as genai
from google.generativeai.types import Tool, FunctionDeclaration
import os
import requests
from dotenv import load_dotenv

# ✅ Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Real-time currency conversion
def convert_currency(from_currency: str, to_currency: str, amount: float) -> str:
    url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or "rates" not in data:
        raise Exception("Failed to fetch exchange rate.")

    rate = data["rates"].get(to_currency.upper(), None)
    if rate is None:
        return f"Currency '{to_currency}' not supported."

    converted = amount * rate
    return f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()} (Rate: {rate:.2f} {to_currency.upper()}/{from_currency.upper()})"

# ✅ Tool registration
conversion_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
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
    ]
)

# ✅ Load Gemini model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    tools=[conversion_tool]
)

# ✅ Streamlit UI
st.title("💱 Currency to PKR Converter")

query = st.text_input("Enter something like: Convert 100 USD to PKR")

if st.button("Get Response"):
    with st.spinner("Thinking..."):
        try:
            convo = model.start_chat()

            # Send structured prompt
            prompt = f"""
You are a currency conversion assistant. When the user gives a query like:
"Convert 50 USD to PKR" or "How much is 200 EUR in PKR"

→ You MUST call the `convert_currency` tool using the extracted values.

Now here is the user's query:
{query}
"""
            response = convo.send_message(prompt)

            # Check for function call
            parts = response.candidates[0].content.parts
            if parts and hasattr(parts[0], 'function_call'):
                call = parts[0].function_call
                if call.name == "convert_currency":
                    from_curr = call.args["from_currency"]
                    to_curr = call.args["to_currency"]
                    amount = float(call.args["amount"])
                    result = convert_currency(from_curr, to_curr, amount)
                    st.success("✅ Result:")
                    st.write(result)
                else:
                    st.warning("Function not recognized.")
            else:
                # fallback: plain text
                st.info("💬 Gemini response:")
                st.write(response.text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
