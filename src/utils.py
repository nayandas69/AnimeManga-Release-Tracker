import json
import os

LAST_SENT_FILE = "data/last_sent.json"


def get_last_sent():
    """Retrieve the list of already sent anime IDs. Create file if missing."""
    if not os.path.exists(LAST_SENT_FILE):
        save_last_sent([])  # Create the file with an empty list

    with open(LAST_SENT_FILE, "r") as file:
        return json.load(file)


def save_last_sent(sent_list):
    """Save the list of sent anime IDs to prevent duplicate notifications."""
    with open(LAST_SENT_FILE, "w") as file:
        json.dump(sent_list, file)
