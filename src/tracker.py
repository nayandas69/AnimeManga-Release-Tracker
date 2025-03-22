import requests
import os
import json
import random
from datetime import datetime, timezone
import pytz
from dotenv import load_dotenv
from utils import get_last_sent, save_last_sent
from notifier import send_discord_notification

# Load environment variables
load_dotenv()

MAL_CLIENT_ID = os.getenv("MAL_CLIENT_ID")

# MyAnimeList API endpoints
API_URL = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=airing&limit=5"
HEADERS = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}


def get_new_releases():
    """Fetch the latest anime releases from MyAnimeList API."""
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []


def get_anime_details(anime_id):
    """Fetch detailed anime information from MyAnimeList API."""
    details_url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=title,main_picture,start_date,genres,rank,score,media_type,num_list_users,next_episode"
    response = requests.get(details_url, headers=HEADERS)
    return response.json() if response.status_code == 200 else {}


def format_next_episode_time(next_episode_timestamp):
    """Convert UTC timestamp to local time and show countdown."""
    if not next_episode_timestamp:
        return "Not Available"

    utc_time = datetime.fromisoformat(next_episode_timestamp.replace("Z", "+00:00"))
    local_time = utc_time.astimezone(
        pytz.timezone("Asia/Dhaka")
    )  # Change to your time zone
    time_left = utc_time - datetime.now(timezone.utc)

    return f"{local_time.strftime('%B %d, %Y %I:%M %p')} ({time_left.days} days left)"


def main():
    last_sent = get_last_sent()
    new_releases = get_new_releases()
    sent_notifications = []

    for anime in new_releases:
        anime_id = anime["node"]["id"]
        if anime_id in last_sent:
            continue

        details = get_anime_details(anime_id)
        if not details:
            continue

        title = details.get("title", "Unknown")
        image_url = details.get("main_picture", {}).get("medium", "")
        anime_url = f"https://myanimelist.net/anime/{anime_id}"
        genres = ", ".join([genre["name"] for genre in details.get("genres", [])])
        anime_type = details.get("media_type", "Unknown").upper()
        score = details.get("score", "N/A")
        rank = details.get("rank", "N/A")
        members = details.get("num_list_users", 0)
        next_episode = format_next_episode_time(details.get("next_episode"))

        send_discord_notification(
            title,
            anime_url,
            image_url,
            genres,
            anime_type,
            score,
            rank,
            members,
            next_episode,
        )
        sent_notifications.append(anime_id)

    if sent_notifications:
        save_last_sent(sent_notifications)


if __name__ == "__main__":
    main()
