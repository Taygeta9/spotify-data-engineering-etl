# Spotify Data Engineering ETL

Pequeño proyecto de ingeniería de datos que construye un pipeline ETL con la API de Spotify para extraer mi historial de reproducciones recientes, transformarlo con Pandas y cargarlo en una base de datos SQLite para análisis.

## Tecnologías

- Python 3.13
- Spotipy (cliente ligero para la Spotify Web API)
- Pandas (transformación y análisis de datos)
- SQLite (almacenamiento tabular)
- Git / GitHub (control de versiones y portafolio)

## Arquitectura del pipeline

El proyecto implementa un flujo ETL básico:

1. **Extract (`extract_spotify.py`)**
   - Autenticación con Spotify usando Authorization Code Flow (Spotipy + Web API).
   - Uso del scope `user-read-recently-played` para obtener las últimas reproducciones del usuario.
   - Persistencia de la respuesta cruda en `recently_played.json`.

2. **Transform (`transform_spotify.py`)**
   - Lectura del JSON crudo y normalización a una estructura tabular con Pandas.
   - Extracción de campos clave:
     - `played_at`, `context_type`, `context_uri`
     - `track_id`, `track_name`, `track_uri`
     - `artist_id`, `artist_name`, `artist_uri`
     - `artist_uri`, `album_name`, `duration_ms`
   - Exportación a `plays_raw.csv` como representación intermedia.

3. **Load (`init_db.py` + `transform_spotify.py`)**
   - Creación de una base de datos SQLite (`spotify_etl.db`).
   - Definición de la tabla `plays_raw`:

     ```sql
     CREATE TABLE IF NOT EXISTS plays_raw (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         played_at TEXT,
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
     ```

   - Inserción de los datos normalizados desde Pandas con `to_sql()` en la tabla `plays_raw`.

## Cómo ejecutar el proyecto

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/Taygeta9/spotify-data-engineering-etl.git
   cd spotify-data-engineering-etl
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # en Windows PowerShell
   ```

3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crear el archivo `.env` en la raíz del proyecto:

   ```env
   client_id=TU_CLIENT_ID_DE_SPOTIFY
   client_secret=TU_CLIENT_SECRET_DE_SPOTIFY
   redirect_uri=http://127.0.0.1:8080/callback
   ```

5. Ejecutar la fase Extract:

   ```bash
   python extract_spotify.py
   ```

   - Se abrirá el navegador para autorizar la app de Spotify.
   - Se generará `recently_played.json` y un archivo `.cache` con el token.

6. Inicializar la base de datos:

   ```bash
   python init_db.py
   ```

7. Ejecutar la fase Transform + Load:

   ```bash
   python transform_spotify.py
   ```

   - Se generará `plays_raw.csv`.
   - Se insertarán los datos en la tabla `plays_raw` de `spotify_etl.db`.

## Próximos pasos / extensiones

Algunas mejoras posibles para evolucionar este proyecto:

- Añadir una tabla de agregados diarios (`user_daily_stats`) con:
  - número de reproducciones por día,
  - minutos escuchados,
  - top artistas y canciones.
- Orquestar el pipeline con Apache Airflow o cron para ejecutarlo de forma periódica.
- Construir visualizaciones (por ejemplo, con Streamlit o dashboards) sobre la base de datos SQLite.
- Añadir tests básicos y validación de calidad de datos.
