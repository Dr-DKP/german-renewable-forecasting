"""
Open-Meteo API Client: Open-Meteo has a free, no-auth API. 
It returns a JSON with an hourly key which contains arrays of values.
Open-Meteo gives us what the weather was doing.
That is the input the XGBoost model will use to predict the residual.
What data we need from Open-Meteo for solar forecasting:

Variable:            Why
shortwave_radiation: Direct measure of solar energy hitting the panel
cloud_cover:         Main reason physics prediction goes wrong
temperature_2m:	     Panels lose efficiency when hot
wind_speed_10m:	     Minor but used by grid operators

API Base URL: https://archive-api.open-meteo.com/v1/archive
"""

import pandas as pd
import requests

# Module level constants
BASE_URL= "https://archive-api.open-meteo.com/v1/archive"


def fetch_weather(lat, lon, start, end) -> pd.DataFrame:
    # build parameters
    params = {
    "latitude": lat,
    "longitude": lon,
    "start_date": start,
    "end_date": end,
    "hourly": "shortwave_radiation,cloud_cover,temperature_2m,wind_speed_10m",
    "timezone": "UTC",
    }
    # execute GET request
    response = requests.get(BASE_URL, params=params)
    # verify the successful request
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: Status {response.status_code}")
    # parse to json with a dict
    raw = response.json()["hourly"]
    # build dataframe
    df_meteo = pd.DataFrame(raw)
    # cleaning data
    df_meteo["time"] = pd.to_datetime(df_meteo["time"], utc = True)
    return df_meteo