import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "spotify_etl.db"

def load_daily_stats():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM user_daily_stats ORDER BY played_date", conn)
    conn.close()
    return df

df_daily = load_daily_stats()

st.title("Spotify Listening Dashboard")

st.subheader("Últimos 7 días")
last_7 = df_daily.tail(7)
st.dataframe(last_7, use_container_width=True)

st.subheader("Últimos 30 días")
last_30 = df_daily.tail(30)
st.dataframe(last_30, use_container_width=True)

st.subheader("Reproducciones por día (últimos 30)")
st.bar_chart(
    last_30.set_index("played_date")["plays_count"]
)

st.subheader("Minutos escuchados por día (últimos 30)")
st.bar_chart(
    last_30.set_index("played_date")["minutes_total"]
)