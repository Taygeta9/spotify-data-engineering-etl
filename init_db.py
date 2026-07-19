import sqlite3

conn = sqlite3.connect("spotify_etl.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS plays_raw (
    played_at TEXT PRIMARY KEY,
    context_type TEXT,
    context_uri TEXT,
    track_id TEXT,
    track_name TEXT,
    track_uri TEXT,
    artist_id TEXT,
    artist_name TEXT,
    artist_uri TEXT,
    album_name TEXT,
    duration_ms INTEGER
);
""")

conn.commit()
conn.close()