import os
import requests
from dotenv import load_dotenv
from utils import get_last_sent, save_last_sent
from notifier import send_discord_notification

load_dotenv()

MAL_CLIENT_ID = os.getenv("MAL_CLIENT_ID")
HEADERS = {"X-MAL-CLIENT-ID": MAL_CLIENT_ID}

ANIME_URL = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=airing&limit=5"
MANGA_URL = (
    "https://api.myanimelist.net/v2/manga/ranking?ranking_type=bypopularity&limit=5"
)


def get_releases(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("data", [])
    except requests.RequestException as e:
        print(f"API Error: {e}")
        return []


def get_details(content_id, category):
    fields = "title,main_picture,genres,rank,score,num_list_users," + (
        "num_episodes,media_type" if category == "anime" else "num_chapters"
    )
    url = f"https://api.myanimelist.net/v2/{category}/{content_id}?fields={fields}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to get details for {category} {content_id}: {e}")
        return {}


def main():
    last_sent = get_last_sent()
    updated = False

    # Anime
    for item in get_releases(ANIME_URL):
        anime_id = str(item["node"]["id"])
        details = get_details(anime_id, "anime")
        if not details:
            continue

        current_count = details.get("num_episodes", 0)
        last_count = last_sent.get("anime", {}).get(anime_id, {}).get("last_episode", 0)

        if current_count > last_count:
            send_discord_notification(
                details.get("title", "Unknown"),
                f"https://myanimelist.net/anime/{anime_id}",
                details.get("main_picture", {}).get("medium", ""),
                ", ".join(g["name"] for g in details.get("genres", [])),
                details.get("media_type", "Unknown").upper(),
                details.get("score", "N/A"),
                details.get("rank", "N/A"),
                details.get("num_list_users", 0),
                current_count,
                "anime",
            )
            last_sent.setdefault("anime", {})[anime_id] = {
                "title": details["title"],
                "last_episode": current_count,
            }
            updated = True

    # Manga
    for item in get_releases(MANGA_URL):
        manga_id = str(item["node"]["id"])
        details = get_details(manga_id, "manga")
        if not details:
            continue

        current_count = details.get("num_chapters", 0)
        last_count = last_sent.get("manga", {}).get(manga_id, {}).get("last_chapter", 0)

        if current_count > last_count:
            send_discord_notification(
                details.get("title", "Unknown"),
                f"https://myanimelist.net/manga/{manga_id}",
                details.get("main_picture", {}).get("medium", ""),
                ", ".join(g["name"] for g in details.get("genres", [])),
                "MANGA",
                details.get("score", "N/A"),
                details.get("rank", "N/A"),
                details.get("num_list_users", 0),
                current_count,
                "manga",
            )
            last_sent.setdefault("manga", {})[manga_id] = {
                "title": details["title"],
                "last_chapter": current_count,
            }
            updated = True

    if updated:
        save_last_sent(last_sent)
        print("Updated last_sent.json")


if __name__ == "__main__":
    main()
