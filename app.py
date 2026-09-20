import os, logging
from flask import Flask, request, jsonify
from config import LIMIT, CHAT_ID, API_KEY
from counter import increment, mark_notified
from notifier import send

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/update")
def update():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify(error="unauthorized"), 401

    body = request.get_json(silent=True) or {}
    d1 = (body.get("data1") or "").strip()
    d2 = (body.get("data2") or "").strip()
    if not d1 and not d2:
        return jsonify(error="empty payload"), 400

    n, notified = increment(CHAT_ID)

    if n >= LIMIT:
        if not notified:
            send(f"Server down\n{LIMIT} messages received")
            mark_notified(CHAT_ID)
            logging.warning("Cap hit (n=%d). Shutdown notice sent.", n)
        return jsonify(status="server_down", n=n), 200

    send(f"New update\n"
         f"Test data 1: {d1}\n"
         f"Test data 2: {d2}\n"
         f"Remaining: {LIMIT - n}")
    logging.info("Sent (n=%d, remaining=%d)", n, LIMIT - n)
    return jsonify(status="sent", n=n, remaining=LIMIT - n), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
