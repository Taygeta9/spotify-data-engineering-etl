import json
import pandas as pd

# 1. Leer el JSON crudo
with open("recently_played.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", [])

print("Items en JSON:", len(items))

# 2. Extraer campos importantes de cada reproducción
rows = []
for item in items:
    track = item.get("track", {})
    artist = track.get("artists", [{}])[0]

    rows.append({
        "played_at": item.get("played_at"),
        "context_type": (item.get("context") or {}).get("type"),
        "context_uri": (item.get("context") or {}).get("uri"),

        "track_id": track.get("id"),
        "track_name": track.get("name"),
        "track_uri": track.get("uri"),

        "artist_id": artist.get("id"),
        "artist_name": artist.get("name"),
        "artist_uri": artist.get("uri"),

        "album_name": (track.get("album") or {}).get("name"),
        "duration_ms": track.get("duration_ms"),
    })

# 3. Crear DataFrame con Pandas
df = pd.DataFrame(rows)
print(df.head())

# 4. Guardar una versión tabular en CSV (para revisar / cargar luego)
df.to_csv("plays_raw.csv", index=False, encoding="utf-8")

import sqlite3

# Conectar a la BD
conn = sqlite3.connect("spotify_etl.db")
cursor = conn.cursor()

# Insertar fila por fila usando INSERT OR IGNORE
insert_sql = """
INSERT OR IGNORE INTO plays_raw (
    played_at,
    context_type,
    context_uri,
    track_id,
    track_name,
    track_uri,
    artist_id,
    artist_name,
    artist_uri,
    album_name,
    duration_ms
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

for _, row in df.iterrows():
    cursor.execute(insert_sql, (
        row["played_at"],
        row["context_type"],
        row["context_uri"],
        row["track_id"],
        row["track_name"],
        row["track_uri"],
        row["artist_id"],
        row["artist_name"],
        row["artist_uri"],
        row["album_name"],
        row["duration_ms"],
    ))

conn.commit()
conn.close()

print("Datos cargados (solo nuevos) en la tabla plays_raw de sqlite.")