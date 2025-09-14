import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="BlackCorp Research")

# ===== Telegram Bot Details =====
BOT_TOKEN = os.getenv("BOT_TOKEN", "8017813507:AAFQy05yhfOvgZOPjLSHnQWr2clIZVY7k9Q")  # Render env var se bhi aa sakta hai
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

# ===== Root Endpoint (Health Check) =====
@app.get("/")
def home():
    return {"status": "ok", "message": "BlackCorp Research bot is live 🚀"}

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


# ===== For Local Run =====
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 9000))  # Local=9000, Render=Render's PORT
    uvicorn.run(app, host="0.0.0.0", port=port)

