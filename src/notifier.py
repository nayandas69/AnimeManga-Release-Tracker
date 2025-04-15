import requests
import os
import random

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def get_random_color():
    """Generate a random color for the Discord embed."""
    return random.randint(0, 0xFFFFFF)


def send_discord_notification(
    title, url, image_url, genres, content_type, score, rank, members, count, category
):
    """Send a rich Discord embed message."""
    count_label = "Episodes" if category == "anime" else "Chapters"

    embed = {
        "title": title,
        "url": url,
        "description": (
            f"**Genres**: {genres}\n"
            f"**Type**: {content_type}\n"
            f"**MAL Score**: {score} | Ranked **#{rank}**\n"
            f"**Members**: {members:,}\n"
            f"**{count_label}**: {count}"
        ),
        "color": get_random_color(),
        "thumbnail": {"url": image_url},
        "footer": {
            "text": "AnimeManga Release Tracker",
            "icon_url": "https://avatars.githubusercontent.com/u/174907517?v=4",  # Icon URL for the footer
        },
    }

    payload = {"embeds": [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code == 204:
            print(f"Notification sent: {title}")
        else:
            print(f"Failed to send: {title} — Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending to Discord for {title}: {e}")
