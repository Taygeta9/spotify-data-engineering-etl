import os
import json
from pathlib import Path

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

client_id = os.getenv("client_id") or os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("client_secret") or os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("redirect_uri") or os.getenv("SPOTIPY_REDIRECT_URI")

if not all([client_id, client_secret, redirect_uri]):
    raise ValueError(
        f"Missing Spotify credentials in {env_path}. "
        "Expected client_id, client_secret, and redirect_uri."
    )

scope = "user-read-recently-played"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
    )
)

results = sp.current_user_recently_played(limit=50)

print("Número de items:", len(results.get("items", [])))

with open("recently_played.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
