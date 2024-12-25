from sqlalchemy import create_engine
import pandas as pd
import sqlalchemy
import sqlite3
from extract import song_df

DATABASE_LOCATION = ""

engine = sqlalchemy.create_engine(DATABASE_LOCATION)
conn = sqlite3.connect("my_songs.sqlite")
cursor = conn.cursor()

sql_query = """"
CREATE TABLE IF EXISTS most_recents(
    song_id TEXT,
    songs_names VARCHAR(30),
    artist_names VARCHAR(30),
    played_at VARCHAR(50),
    timestamps TIMESTAMP
)
"""

cursor.execute(sql_query)
try:
    song_df.to_sql("most_recents"engine,index="False",if_exists="append")
except:
    print("Data already exists in the s")