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