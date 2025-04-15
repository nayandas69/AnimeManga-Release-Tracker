import os
import json

LAST_SENT_FILE = "data/last_sent.json"


def get_last_sent():
    if not os.path.exists(LAST_SENT_FILE):
        save_last_sent({"anime": {}, "manga": {}})
    try:
        with open(LAST_SENT_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {"anime": {}, "manga": {}}
    except (json.JSONDecodeError, FileNotFoundError):
        return {"anime": {}, "manga": {}}


def save_last_sent(data):
    with open(LAST_SENT_FILE, "w") as f:
        json.dump(data, f, indent=4)
