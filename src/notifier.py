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
    """Send a rich Discord embed notification with detailed anime or manga info."""
    count_label = "Episodes" if category == "anime" else "Chapters"

    embed = {
        "title": title,
        "url": url,
        "description": (
            f" **Genres**: {genres}\n"
            f" **Type**: {content_type}\n"
            f" **MAL Score**: {score} | Ranked **#{rank}**\n"
            f" **Members**: {members}\n"
            f" **{count_label}**: {count}"
        ),
        "color": get_random_color(),
        "thumbnail": {"url": image_url},
        "footer": {"text": "AnimeManga Release Tracker"},
    }

    payload = {"embeds": [embed]}
    response = requests.post(DISCORD_WEBHOOK, json=payload)

    if response.status_code == 204:
        print(f"✅ Sent notification for {title}")
    else:
        print(f"❌ Failed to send notification for {title}: {response.status_code}")
