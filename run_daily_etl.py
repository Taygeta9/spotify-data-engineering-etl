#!/usr/bin/env python

import subprocess
import sys

python_exe = sys.executable

result_init = subprocess.run(
    [python_exe, "init_db.py"],
    check=False
)
print("init_db.py return code:", result_init.returncode)

result_extract = subprocess.run(
    [python_exe, "extract_spotify.py"],
    check=False
)
print("extract_spotify.py return code:", result_extract.returncode)

result_transform = subprocess.run(
    [python_exe, "transform_spotify.py"],
    check=False
)
print("transform_spotify.py return code:", result_transform.returncode)

result_daily = subprocess.run(
    [python_exe, "build_daily_stats.py"],
    check=False
)
print("build_daily_stats.py return code:", result_daily.returncode)