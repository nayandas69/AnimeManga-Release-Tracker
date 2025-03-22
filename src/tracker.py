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
HEADERS = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}
API_URL = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=airing&limit=10"


def get_new_releases():
    """Fetch the latest anime releases from MyAnimeList API."""
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []


def get_anime_details(anime_id):
    """Fetch detailed anime information from MyAnimeList API."""
    details_url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=title,main_picture,start_date,genres,rank,score,media_type,num_list_users,nsfw,studios,episodes,next_episode"
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

    for anime in new_releases:
        anime_id = anime["node"]["id"]
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
        episode_number = details.get("episodes", 0)  # Latest available episode

        # Skip if no new episode is available
        if (
            anime_id in last_sent
            and last_sent[anime_id]["last_episode"] >= episode_number
        ):
            continue  # Already notified this episode

        # Send Discord notification
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

        # Update last_sent.json with latest episode number
        last_sent[anime_id] = {"title": title, "last_episode": episode_number}
        save_last_sent(last_sent)


if __name__ == "__main__":
    main()
