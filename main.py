import sys, logging
from config import LIMIT
from counter import increment
from notifier import send

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def handle(user_id: str, data1: str, data2: str) -> None:
    n = increment(user_id)

    if n >= LIMIT:
        ok = send(f"Server down\n{LIMIT} messages received\nUser: {user_id}")
        logging.warning("Cap hit for %s (n=%d). Notified=%s. Exiting.", user_id, n, ok)
        sys.exit(0)

    send(
        f"New update\n"
        f"Test data 1: {data1}\n"
        f"Test data 2: {data2}\n"
        f"Remaining: {LIMIT - n}"
    )
    logging.info("Sent for %s (n=%d, remaining=%d)", user_id, n, LIMIT - n)

if __name__ == "__main__":
    user_id = input("User ID: ").strip()
    while True:
        try:
            d1 = input("Test data 1: ").strip()
            d2 = input("Test data 2: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nStopped.")
            break

        if not d1 and not d2:
            print("Empty input, stopping.")
            break

        handle(user_id, d1, d2)
