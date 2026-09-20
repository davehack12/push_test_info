import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
LIMIT     = int(os.environ.get("LIMIT", "20"))
DB_PATH   = os.environ.get("DB_PATH", "counter.db")
API_KEY   = os.environ["API_KEY"]
