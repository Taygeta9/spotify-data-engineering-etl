import sqlite3
import pandas as pd

DB_PATH = "spotify_etl.db"  # mismo nombre que init_db y dashboard

# 1. Conectar a la base de datos SQLite
conn = sqlite3.connect(DB_PATH)

# 2. Leer las reproducciones crudas desde plays_raw
df = pd.read_sql_query("""
    SELECT played_at, duration_ms
    FROM plays_raw
""", conn)

# 3. Convertir played_at (texto ISO) a datetime y extraer solo la fecha (AAAA-MM-DD)
df["played_date"] = pd.to_datetime(df["played_at"]).dt.date

# 4. Agrupar por played_date:
#    - plays_count: número de reproducciones por día
#    - minutes_total: minutos totales escuchados por día
daily_stats = df.groupby("played_date").agg(
    plays_count=("played_at", "count"),
    minutes_total=("duration_ms", lambda x: x.sum() / 60000.0),
).reset_index()

print("Estadísticas diarias calculadas:")
print(daily_stats)

# 5. Guardar el resultado en la tabla user_daily_stats
daily_stats.to_sql("user_daily_stats", conn, if_exists="replace", index=False)

conn.close()

print("Tabla user_daily_stats creada/actualizada en sqlite.")