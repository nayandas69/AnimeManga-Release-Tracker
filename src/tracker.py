import os
import json
import requests
from dotenv import load_dotenv
from utils import get_last_sent, save_last_sent
from notifier import send_discord_notification

# Load environment variables from .env or GitHub Secrets
load_dotenv()

MAL_CLIENT_ID = os.getenv("MAL_CLIENT_ID")
HEADERS = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}

# API URLs for anime and manga rankings
ANIME_API_URL = (
    "https://api.myanimelist.net/v2/anime/ranking?ranking_type=airing&limit=5"
)
MANGA_API_URL = (
    "https://api.myanimelist.net/v2/manga/ranking?ranking_type=bypopularity&limit=5"
)


def fetch_json(url):
    """Helper to safely fetch JSON data."""
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return {}


def get_detailed_anime(anime_id):
    """Fetch detailed anime info from MAL."""
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=title,main_picture,genres,rank,score,media_type,num_list_users,num_episodes"
    return fetch_json(url)


def get_detailed_manga(manga_id):
    """Fetch detailed manga info from MAL."""
    url = f"https://api.myanimelist.net/v2/manga/{manga_id}?fields=title,main_picture,genres,rank,score,num_list_users,num_chapters"
    return fetch_json(url)


def main():
    last_sent = get_last_sent()
    sent_notifications = False

    # Check Anime Releases
    anime_data = fetch_json(ANIME_API_URL).get("data", [])
    for item in anime_data:
        node = item["node"]
        anime_id = str(node["id"])
        details = get_detailed_anime(anime_id)
        if not details:
            continue

        title = details.get("title", "Unknown")
        image_url = details.get("main_picture", {}).get("medium", "")
        url = f"https://myanimelist.net/anime/{anime_id}"
        genres = ", ".join([g["name"] for g in details.get("genres", [])])
        media_type = details.get("media_type", "Unknown").upper()
        score = details.get("score", "N/A")
        rank = details.get("rank", "N/A")
        members = details.get("num_list_users", 0)
        episodes = details.get("num_episodes", 0)

        last_episode_sent = (
            last_sent.get("anime", {}).get(anime_id, {}).get("last_episode", 0)
        )

        if episodes > last_episode_sent:
            send_discord_notification(
                title,
                url,
                image_url,
                genres,
                media_type,
                score,
                rank,
                members,
                episodes,
                "anime",
            )
            last_sent.setdefault("anime", {})[anime_id] = {
                "title": title,
                "last_episode": episodes,
            }
            sent_notifications = True

    # Check Manga Releases
    manga_data = fetch_json(MANGA_API_URL).get("data", [])
    for item in manga_data:
        node = item["node"]
        manga_id = str(node["id"])
        details = get_detailed_manga(manga_id)
        if not details:
            continue

        title = details.get("title", "Unknown")
        image_url = details.get("main_picture", {}).get("medium", "")
        url = f"https://myanimelist.net/manga/{manga_id}"
        genres = ", ".join([g["name"] for g in details.get("genres", [])])
        score = details.get("score", "N/A")
        rank = details.get("rank", "N/A")
        members = details.get("num_list_users", 0)
        chapters = details.get("num_chapters", 0)

        last_chapter_sent = (
            last_sent.get("manga", {}).get(manga_id, {}).get("last_chapter", 0)
        )

        if chapters > last_chapter_sent:
            send_discord_notification(
                title,
                url,
                image_url,
                genres,
                "MANGA",
                score,
                rank,
                members,
                chapters,
                "manga",
            )
            last_sent.setdefault("manga", {})[manga_id] = {
                "title": title,
                "last_chapter": chapters,
            }
            sent_notifications = True

    # Save updated state if something was sent
    if sent_notifications:
        save_last_sent(last_sent)


if __name__ == "__main__":
    main()
