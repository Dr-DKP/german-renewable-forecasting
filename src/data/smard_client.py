"""
SMARD API Client — Bundesnetzagentur electricity market data.

Fetches hourly generation data (solar, wind onshore, wind offshore)
from Germany's official Strommarktdaten platform.

API docs: https://www.smard.de/app/help/en
"""

import requests
import pandas as pd
BASE_URL = "https://www.smard.de/app/chart_data"
SOLAR_FILTER = 4068
REGION = "DE"
RESOLUTION = "hour"
def get_available_timestamps() -> list[int]:
    """
    Fetch the index of available data chunks from SMARD
    Returns a list of timestamps in ms, each represents one week of data
    """
    # built url using f-string
    url = f"{BASE_URL}/{SOLAR_FILTER}/{REGION}/index_{RESOLUTION}.json"
    # execute GET request
    response = requests.get(url)
    # verify the successful request
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: Status {response.status_code}")
    
    # parse json and return the specific key
    data = response.json()
    return data["timestamps"]

def fetch_chunk(timestamp_ms: int) -> pd.DataFrame:
    """
    Fetch one week of hourly solar data for a given chunk timestamp.
    Returns a dataframe with columns: time (UTC) and solar_mw.  
    """
    # build the url
    url = f"{BASE_URL}/{SOLAR_FILTER}/{REGION}/{SOLAR_FILTER}_{REGION}_{RESOLUTION}_{timestamp_ms}.json"
    # request the data
    response = requests.get(url)
    response.raise_for_status() #shortcut for checking status code (200)
    # get access to the "series" key
    raw_data = response.json()["series"]
    # build DataFrame that converts ms timestamps to timestamps and solar_mw
    df = pd.DataFrame(raw_data, columns=["time", "solar_mw"])
    # cleaning data
    df["time"] = pd.to_datetime(df["time"], unit='ms', utc = True)

    # get final dat
    return df

def fetch_solar_generation(start: str, end: str) -> pd.DataFrame:
    """
    Fetch all horly data of solar generation between start and end dates
    start/end format: "YYYY-MM-DD"
    Returned concatenated DataFrame sorted by time and filtered with start and end.
    """
    # define start and end dates
    start_dt = pd.Timestamp(start, tz="UTC")
    end_dt = pd.Timestamp(end, tz="UTC")
    # get the index of available weeks
    all_weeks = get_available_timestamps()
    # filter list and fetch data
    chunks = []
    for ts in all_weeks:
        #Convert the week's timestamp (ts) to a date to compare
        week_dt = pd.to_datetime(ts, unit="ms", utc=True)
        # If the week is within a reasonable range of the request
        if week_dt >= (start_dt - pd.Timedelta(days=7)) and week_dt <= end_dt:
            df_chunk = fetch_chunk(ts)
            chunks.append(df_chunk)
    # combine everything
    full_df = pd.concat(chunks).sort_values("time")

    # final trim to match the request
    mask = (full_df["time"] >= start_dt) & (full_df["time"] <= end_dt)
    return full_df.loc[mask].reset_index(drop = True)