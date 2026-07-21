# Spotify Data Engineering ETL

Pequeño proyecto de ingeniería de datos que construye un pipeline ETL con la API de Spotify para extraer mi historial de reproducciones recientes, transformarlo con Pandas, cargarlo en una base de datos SQLite y visualizar estadísticas básicas en un dashboard con Streamlit.

## Tecnologías

- Python 3.13
- Spotipy / Spotify Web API
- Pandas (transformación y análisis de datos)
- SQLite (almacenamiento tabular)
- Streamlit (dashboard web sencillo)
- Git / GitHub + GitHub Actions (control de versiones y ejecución programada)

## Arquitectura del pipeline

El proyecto implementa un flujo ETL básico sobre mi historial de “recently played”:

1. **Extract (`extract_spotify.py`)**
   - Autenticación con Spotify usando Authorization Code Flow.
   - Uso del scope `user-read-recently-played` para obtener las últimas reproducciones del usuario.
   - Persistencia de la respuesta cruda en `recently_played.json`.

2. **Transform + Load a reproducciones crudas (`transform_spotify.py` + `init_db.py`)**
   - Lectura del JSON crudo y normalización a una estructura tabular con Pandas.
   - Extracción de campos clave como:
     - `played_at`, `context_type`, `context_uri`
     - `track_id`, `track_name`, `track_uri`
     - `artist_name`
     - `album_name`, `duration_ms`
   - Creación de la base SQLite `spotify_etl.db` y de la tabla `plays_raw` (desde `init_db.py`), y carga de los datos normalizados con `to_sql()` en `plays_raw`.

3. **Agregados diarios (`build_daily_stats.py`)**
   - Lectura de `plays_raw` desde SQLite.
   - Conversión de `played_at` a fecha (`played_date`).
   - Cálculo de:
     - `plays_count`: número de reproducciones por día.
     - `minutes_total`: minutos totales escuchados por día (a partir de `duration_ms`).
   - Escritura de los resultados en la tabla `user_daily_stats` dentro de `spotify_etl.db`.

4. **Orquestación (`run_daily_etl.py`)**
   - Script maestro que ejecuta secuencialmente:
     1. `init_db.py` (asegura esquema mínimo).
     2. `extract_spotify.py` (actualiza `recently_played.json`).
     3. `transform_spotify.py` (llena `plays_raw`).
     4. `build_daily_stats.py` (actualiza `user_daily_stats`).
   - Usa `sys.executable` para garantizar que todos los pasos corren dentro del mismo entorno virtual de Python.

5. **Dashboard (`dashboard.py`)**
   - Lee la tabla `user_daily_stats` desde `spotify_etl.db`.
   - Muestra:
     - Tabla resumen de los últimos **7 días**.
     - Tabla resumen de los últimos **30 días**.
     - Gráficos de barras de `plays_count` y `minutes_total` por día (últimos 30 días) usando `st.bar_chart`.

## Setup local

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
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Crear el archivo `.env` en la raíz del proyecto (no se versiona, solo local):

   ```env
   SPOTIFY_CLIENT_ID=TU_CLIENT_ID_DE_SPOTIFY
   SPOTIFY_CLIENT_SECRET=TU_CLIENT_SECRET_DE_SPOTIFY
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:8080/callback
   ```

   Para referencia, el repo incluye un `.env.example` con los nombres de variables esperadas.

5. Ejecutar el ETL completo de forma manual:

   ```bash
   python run_daily_etl.py
   ```

   Esto:
   - Inicializa la base (`spotify_etl.db`) y las tablas mínimas.
   - Descarga tus últimas reproducciones.
   - Carga en `plays_raw`.
   - Calcula y guarda agregados diarios en `user_daily_stats`.

6. Ejecutar el dashboard con Streamlit:

   ```bash
   streamlit run dashboard.py
   ```

   Se abrirá un dashboard local donde se muestran las tablas de últimos 7 y 30 días y gráficos de barras básicos.

## Ejecución programada con GitHub Actions (opcional)

El proyecto puede ejecutarse automáticamente una vez al día usando GitHub Actions:

1. Definir secrets en GitHub (Settings → Secrets and variables → Actions):

   - `SPOTIFY_CLIENT_ID`
   - `SPOTIFY_CLIENT_SECRET`

2. Crear un workflow (por ejemplo `.github/workflows/daily-etl.yml`) que:

   - Use un disparador `schedule` (cron) para correr una vez al día.
   - Configure las variables de entorno a partir de los secrets.
   - Instale dependencias y ejecute `python run_daily_etl.py`.

El código del proyecto está preparado para leer las credenciales desde variables de entorno, por lo que funciona tanto en local (con `.env` + `python-dotenv`) como en GitHub Actions (con `env` + `secrets`).

## Alcance actual y posibles extensiones

**Lo que hace hoy el proyecto:**

- Extrae mi historial reciente de reproducciones desde la API de Spotify.
- Normaliza y guarda todos los plays en una tabla `plays_raw` en SQLite.
- Calcula estadísticas diarias básicas en `user_daily_stats`.
- Expone un dashboard simple con Streamlit para explorar últimos días y tendencias.

**Ideas futuras (no implementadas todavía):**

- Añadir más métricas diarias (por ejemplo, top artistas/canciones por día).
- Construir dashboards más completos (por ejemplo, con más filtros y vistas).
- Revisar integraciones con otros almacenes (data lake, warehouse) o con herramientas de orquestación más avanzadas.

