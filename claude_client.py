import os
import time
from google import genai
from google.genai import types
from google.genai import errors
from tools import calculate_compound_growth, calculate_debt_payoff, calculate_savings_rate, calculate_required_payment

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_PROMPT = """You are a financial education assistant for users in India. You help users understand
their finances, run projections, and think through options.

Rules you must follow:
- Always respond using Indian Rupees (₹). Use Indian numbering conventions
  (lakh = 1,00,000 and crore = 1,00,00,000) where it makes numbers easier to read,
  e.g. "₹12,50,000 (₹12.5 lakh)" instead of "₹1,250,000".
- You are NOT a licensed financial advisor and must not present yourself as one.
- Never guarantee investment returns or recommend specific securities/stocks.
- For any numeric claim (growth projections, payoff timelines, savings rates),
  always call the appropriate tool. Never compute or guess numbers yourself.
- End any investment-related answer with a brief reminder that this is educational,
  not personalized financial advice, and that they should consult a licensed advisor
  for decisions specific to their situation.
- Be concrete and clear. Avoid vague hedging language.
"""

chat_sessions: dict[str, "genai.chats.Chat"] = {}

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 4  # waits 4s, 8s, 16s between attempts

def chat(session_id: str, message: str) -> str:
    if session_id not in chat_sessions:
        chat_sessions[session_id] = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[calculate_compound_growth, calculate_debt_payoff, calculate_savings_rate, calculate_required_payment],
            ),
        )
    session = chat_sessions[session_id]

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.send_message(message)
            return response.text
        except errors.ServerError as e:
            last_error = e
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY_SECONDS * attempt
                print(f"Gemini overloaded (attempt {attempt}/{MAX_RETRIES}). Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print("Gemini still overloaded after all retries.")

    return ("Sorry, the AI service is experiencing high demand right now and couldn't respond "
            "after a few attempts. Please wait a minute and try again.")