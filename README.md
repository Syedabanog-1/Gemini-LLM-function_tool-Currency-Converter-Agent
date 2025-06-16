
# Gemini-LLM-function_tool-Currency-Converter-Agent


 Program Objective
This program is an intelligent currency converter assistant that understands user queries written in natural language (e.g., "Convert 100 USD to PKR") and provides real-time currency conversion using up-to-date exchange rates.
It uses Google Gemini AI and Streamlit to deliver an interactive, AI-powered experience.

⚙️ Core Functionalities
1. 🧠 Natural Language Understanding with Gemini
Accepts user queries written in plain English.

Gemini AI analyzes the query to extract relevant data: from_currency, to_currency, and amount.

2. 🔗 Tool Calling by Gemini
Gemini is configured with a custom tool convert_currency.

When a conversion query is detected, Gemini automatically calls this tool with extracted values.

3. 🌐 Live Exchange Rate Fetching
Uses https://open.er-api.com to fetch the most recent exchange rates.

If the target currency is not supported or the API fails, the program handles it gracefully.

4. 🖥️ Streamlit-Based UI
Simple and clean user interface includes:

Text input for user queries

“Get Response” button

Loading spinner

Final result display with success or error message

5. ✅ Sample Output
User Query: Convert 50 USD to PKR
Result: 50 USD = 14000.00 PKR (Rate: 280.00 PKR/USD)

6. 🚨 Error Handling
If something goes wrong (API failure, invalid currency, Gemini misresponse), a proper error message is displayed.

🧱 Technology Stack
Technology	Purpose
Streamlit	Building the web-based user interface
Google Gemini AI	Natural language processing and tool calling
dotenv	Securely loading environment variables
Requests	Making HTTP calls to get live exchange rates
ER-API	External API used for real-time currency rates

💡 Key Highlights
✅ AI-assisted, user-friendly interface

✅ Function tool integration with Gemini

✅ Real-time, accurate conversion rates

✅ Minimalist and functional UI

![pkr to usd](https://github.com/user-attachments/assets/f610c92e-3fe4-4348-9258-ecaba2aa5b10)
![200 USD to PKR](https://github.com/user-attachments/assets/14019304-94b1-449f-b686-1330e03941d0)
![TODAYS DOLLAR RATE](https://github.com/user-attachments/assets/53aabaa7-921a-4742-b7aa-36fc370f2ad1)
![USD TO PKR](https://github.com/user-attachments/assets/95c64d02-85b6-4614-8ae7-6a1c5bbd3bea)
![EUR to PKR](https://github.com/user-attachments/assets/562d7538-10ba-4d31-bfa3-845493d64566)
