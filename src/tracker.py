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
    details_url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=title,main_picture,start_date,genres,rank,score,media_type,num_list_users,num_episodes"
    response = requests.get(details_url, headers=HEADERS)
    return response.json() if response.status_code == 200 else {}


def format_next_episode_time(utc_timestamp):
    """Convert UTC timestamp to local time and show countdown."""
    if not utc_timestamp:
        return "Not Available"

    utc_time = datetime.fromisoformat(utc_timestamp.replace("Z", "+00:00"))
    local_time = utc_time.astimezone(pytz.timezone("Asia/Dhaka"))  # Change time zone
    time_left = utc_time - datetime.now(timezone.utc)

    return f"{local_time.strftime('%B %d, %Y %I:%M %p')} ({time_left.days} days left)"


def main():
    last_sent = get_last_sent()  # Load previously sent notifications
    new_releases = get_new_releases()
    sent_notifications = False  # Flag to check if any updates were sent

    for anime in new_releases:
        anime_id = str(anime["node"]["id"])  # Ensure anime_id is a string

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
        num_episodes = details.get("num_episodes", "N/A")

        # If this anime is already in last_sent.json, check for new episodes
        last_episode_sent = last_sent.get(anime_id, {}).get("last_episode", 0)

        # Send notification only if a new episode is detected
        if num_episodes == "N/A" or num_episodes <= last_episode_sent:
            continue  # Skip if no new episode

        send_discord_notification(
            title,
            anime_url,
            image_url,
            genres,
            anime_type,
            score,
            rank,
            members,
            num_episodes,
        )
        last_sent[anime_id] = {"title": title, "last_episode": num_episodes}
        sent_notifications = True

    # Save updated last_sent.json if new notifications were sent
    if sent_notifications:
        save_last_sent(last_sent)


if __name__ == "__main__":
    main()
