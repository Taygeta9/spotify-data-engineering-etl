#!/usr/bin/env python

import subprocess

# 0. Llamar a la API de Spotify y actualizar recently_played.json
result_extract = subprocess.run(
    ["python", "extract_spotify.py"],
    check=False
)
print("extract_spotify.py return code:", result_extract.returncode)

# 1. Ejecutar el ETL que transforma y carga en plays_raw
result_transform = subprocess.run(
    ["python", "transform_spotify.py"],
    check=False
)
print("transform_spotify.py return code:", result_transform.returncode)

# 2. Ejecutar el script que construye la tabla user_daily_stats
result_daily = subprocess.run(
    ["python", "build_daily_stats.py"],
    check=False
)
print("build_daily_stats.py return code:", result_daily.returncode)