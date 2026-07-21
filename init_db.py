import sqlite3

DB_PATH = "spotify_etl.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabla base con todas las reproducciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plays_raw (
            play_id TEXT PRIMARY KEY,
            played_at TEXT NOT NULL,
            track_id TEXT NOT NULL,
            track_name TEXT,
            artist_name TEXT,
            ms_played INTEGER,
            context TEXT
        )
    """)

    # Tabla agregada por día
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_daily_stats (
            play_date TEXT PRIMARY KEY,
            total_plays INTEGER NOT NULL,
            total_ms_played INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()