import json
import os

LAST_SENT_FILE = "data/last_sent.json"


def get_last_sent():
    """Retrieve the dictionary of last notified anime episodes. Auto-create file if missing."""
    if not os.path.exists(LAST_SENT_FILE):
        save_last_sent({})  # Create an empty dictionary

    with open(LAST_SENT_FILE, "r") as file:
        return json.load(file)


def save_last_sent(sent_data):
    """Save the dictionary of last notified anime episodes to prevent duplicate messages."""
    with open(LAST_SENT_FILE, "w") as file:
        json.dump(sent_data, file, indent=4)  # Pretty format JSON
