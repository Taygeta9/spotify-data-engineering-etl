import sqlite3

conn = sqlite3.connect("spotify_etl.db")
cursor = conn.cursor()

# 1. Ver cuántas filas hay en la tabla
cursor.execute("SELECT COUNT(*) FROM plays_raw;")
count = cursor.fetchone()[0]
print("Filas en plays_raw:", count)

# 2. Ver algunas filas de muestra
cursor.execute("""
SELECT played_at, track_name, artist_name
FROM plays_raw
ORDER BY played_at DESC
LIMIT 5;
""")

rows = cursor.fetchall()
print("Muestras recientes:")
for row in rows:
    print(row)

conn.close()