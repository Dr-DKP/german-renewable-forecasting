
# Import Libraries
import psycopg2
import pandas as pd
from pathlib import Path

# Constant DB URL
DB_URL = "postgresql://solar:solar@localhost:5432/solar_db"

def ingest_solar(conn) -> pd.DataFrame:
    df = pd.read_parquet(Path(__file__).parent.parent.parent / "data/raw/solar_2022_2024.parquet").reset_index() # reset index sp `time` becomes a regular columns
    data_tuples = list(df[["time", "solar_mw"]].itertuples(index=False, name=None))
    # create cursor and execute insertion
    cur = conn.cursor()
    sql = "INSERT INTO solar_generation (time, solar_mw) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    cur.executemany(sql, data_tuples)
    conn.commit()
    print(f"Ingested {len(data_tuples)} new rows into solar_generation.")
    cur.close()

def ingest_weather(conn):
    # resolve path and load data
    data_path = Path(__file__).parent.parent.parent / "data/raw/weather_2022_2024.parquet"
    df = pd.read_parquet(data_path)
    
    # Prepare data
    df = df.reset_index()
    cols = ["time", "shortwave_radiation", "cloud_cover", "temperature_2m", "wind_speed_10m"]
    data_tuples = list(df[cols].itertuples(index=False, name=None))
    # Execute insertion
    cur = conn.cursor()
    sql = """
        INSERT INTO weather_observations 
        (time, shortwave_radiation, cloud_cover, temperature_2m, wind_speed_10m) 
        VALUES (%s, %s, %s, %s, %s) 
        ON CONFLICT DO NOTHING
    """
    
    cur.executemany(sql, data_tuples)
    conn.commit()
    
    print(f"Ingested {len(data_tuples)} new rows into weather_observations.")
    cur.close()

if __name__ == "__main__":
    # The 'with' block ensures the connection is closed even if an error pops up
    try:
        with psycopg2.connect(DB_URL) as conn:
            print("Connected to PostgreSQL. Starting ingestion...")
            ingest_solar(conn)
            ingest_weather(conn)
            print("Ingestion complete.")
    except Exception as e:
        print(f"An error occurred: {e}")