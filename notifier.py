import requests
from config import BOT_TOKEN, CHAT_ID

def send(text: str) -> bool:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        return r.ok
    except requests.RequestException:
        return False
