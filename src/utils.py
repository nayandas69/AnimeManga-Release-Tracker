import os
import json

LAST_SENT_FILE = "data/last_sent.json"


def get_last_sent():
    """Retrieve the last sent notifications from JSON file."""
    if not os.path.exists(LAST_SENT_FILE):
        save_last_sent({"anime": {}, "manga": {}})
        return {"anime": {}, "manga": {}}

    try:
        with open(LAST_SENT_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {"anime": {}, "manga": {}}
    except (json.JSONDecodeError, IOError):
        return {"anime": {}, "manga": {}}


def save_last_sent(sent_dict):
    """Save the updated notifications to JSON file."""
    try:
        with open(LAST_SENT_FILE, "w") as file:
            json.dump(sent_dict, file, indent=4)
    except Exception as e:
        print(f"Failed to save last_sent.json: {e}")
