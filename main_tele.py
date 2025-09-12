from fastapi import FastAPI
from pydantic import BaseModel
import requests
from typing import List

app = FastAPI(title="BlackCorp Research")

# ===== Telegram Bot Details =====
BOT_TOKEN = "8017813507:AAFQy05yhfOvgZOPjLSHnQWr2clIZVY7k9Q"
CHAT_IDS = ["@blackcorpResearch"]  # Add multiple client chat_ids here

def send_telegram_message(message: str):
    """Send message to all Telegram clients"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        payload = {"chat_id": chat_id, "text": message}
        try:
            requests.post(url, data=payload, timeout=10)
        except Exception as e:
            print(f"❌ Error sending message to {chat_id}: {e}")

# ===== Pydantic Model for TradingView Payload =====
class TradingViewPayload(BaseModel):
    secret: str
    symbol: str
    action: str
    price: str

# ===== Webhook Endpoint =====
@app.post("/webhook")
async def webhook(payload: TradingViewPayload):
    # Secret Key Check
    if payload.secret != "my_secret_key":
        return {"status": "error", "message": "Invalid secret"}

    # Build Telegram Message
    message = f"""
📢 Trading Signal Alert
Symbol: {payload.symbol}
Action: {payload.action}
Price: {payload.price}
"""
    send_telegram_message(message.strip())

    return {"status": "success", "message": "Signal sent to Telegram"}
