import sqlite3
import pandas as pd

# 1. Conectar y leer la tabla
conn = sqlite3.connect("spotify_etl.db")
df = pd.read_sql("SELECT * FROM plays_raw;", conn)
conn.close()

print("Filas cargadas desde plays_raw:", len(df))
print("Columnas:", df.columns.tolist())
print("\nPrimeras 5 filas:")
print(df.head())

# 2. Minutos por artista
df["duration_ms"] = pd.to_numeric(df["duration_ms"], errors="coerce")

artist_time = (
    df.groupby("artist_name")["duration_ms"]
    .sum()
    .sort_values(ascending=False)
    / 1000 / 60
)

print("\nTop 5 artistas por minutos escuchados:")
print(artist_time.head(5))

# 3. Top canciones por número de reproducciones
track_counts = (
    df.groupby(["track_name", "artist_name"])
    .size()
    .sort_values(ascending=False)
)

print("\nTop 5 canciones por cantidad de reproducciones:")
print(track_counts.head(5))

# 4. Minutos totales
total_minutes = df["duration_ms"].sum() / 1000 / 60
print(f"\nMinutos totales escuchados en este dataset: {total_minutes:.2f}")