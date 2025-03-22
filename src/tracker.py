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
ANIME_API_URL = (
    "https://api.myanimelist.net/v2/anime/ranking?ranking_type=airing&limit=5"
)
MANGA_API_URL = (
    "https://api.myanimelist.net/v2/manga/ranking?ranking_type=bypopularity&limit=5"
)
HEADERS = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}


def get_new_releases(api_url):
    """Fetch latest anime or manga releases from MyAnimeList API."""
    response = requests.get(api_url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []


def get_anime_details(anime_id):
    """Fetch detailed anime information from MyAnimeList API."""
    details_url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=title,main_picture,genres,rank,score,media_type,num_list_users,num_episodes"
    response = requests.get(details_url, headers=HEADERS)
    return response.json() if response.status_code == 200 else {}


def get_manga_details(manga_id):
    """Fetch detailed manga information from MyAnimeList API."""
    details_url = f"https://api.myanimelist.net/v2/manga/{manga_id}?fields=title,main_picture,genres,rank,score,num_list_users,num_chapters"
    response = requests.get(details_url, headers=HEADERS)
    return response.json() if response.status_code == 200 else {}


def main():
    last_sent = get_last_sent()  # Load previously sent notifications
    new_anime = get_new_releases(ANIME_API_URL)
    new_manga = get_new_releases(MANGA_API_URL)
    sent_notifications = False  # Flag to check if any updates were sent

    # 🔹 Check Anime Releases
    for anime in new_anime:
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
        num_episodes = details.get("num_episodes", 0)

        last_episode_sent = (
            last_sent.get("anime", {}).get(anime_id, {}).get("last_episode", 0)
        )

        if num_episodes > last_episode_sent:
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
                "anime",
            )
            last_sent.setdefault("anime", {})[anime_id] = {
                "title": title,
                "last_episode": num_episodes,
            }
            sent_notifications = True

    # 🔹 Check Manga Releases
    for manga in new_manga:
        manga_id = str(manga["node"]["id"])

        details = get_manga_details(manga_id)
        if not details:
            continue

        title = details.get("title", "Unknown")
        image_url = details.get("main_picture", {}).get("medium", "")
        manga_url = f"https://myanimelist.net/manga/{manga_id}"
        genres = ", ".join([genre["name"] for genre in details.get("genres", [])])
        score = details.get("score", "N/A")
        rank = details.get("rank", "N/A")
        members = details.get("num_list_users", 0)
        num_chapters = details.get("num_chapters", 0)

        last_chapter_sent = (
            last_sent.get("manga", {}).get(manga_id, {}).get("last_chapter", 0)
        )

        if num_chapters > last_chapter_sent:
            send_discord_notification(
                title,
                manga_url,
                image_url,
                genres,
                "MANGA",
                score,
                rank,
                members,
                num_chapters,
                "manga",
            )
            last_sent.setdefault("manga", {})[manga_id] = {
                "title": title,
                "last_chapter": num_chapters,
            }
            sent_notifications = True

    if sent_notifications:
        save_last_sent(last_sent)


if __name__ == "__main__":
    main()
