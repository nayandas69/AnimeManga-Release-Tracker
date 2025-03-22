import json
import os

LAST_SENT_FILE = "data/last_sent.json"


def get_last_sent():
    """Retrieve stored last sent notifications. Ensure it returns a dictionary."""
    if not os.path.exists(LAST_SENT_FILE):
        save_last_sent({})  # Store as an empty dictionary instead of a list

    with open(LAST_SENT_FILE, "r") as file:
        try:
            data = json.load(file)
            return data if isinstance(data, dict) else {}  # Ensure dictionary format
        except json.JSONDecodeError:
            return {}  # Return empty dictionary if file is corrupted


def save_last_sent(sent_dict):
    """Save the list of sent anime episodes to prevent duplicate notifications."""
    with open(LAST_SENT_FILE, "w") as file:
        json.dump(sent_dict, file, indent=4)
