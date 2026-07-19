#!/usr/bin/env python

import subprocess

# 1. Ejecutar el ETL que descarga de la API y carga en plays_raw
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