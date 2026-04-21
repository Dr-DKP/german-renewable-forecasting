"""
Tests if openmeteo_client.py works as it should be. 
It should return a DataFrame, a time coulumn, time is timezone aware
and has all 4 weather columns.
"""


# Import libraries
import pandas as pd
import pytest
from src.data.openmeteo_client import fetch_weather


def test_fetch_weather():
    lat = "51.2"
    lan = "10.2"
    start_date = "2024-01-01"
    end_date = "2024-01-03"
    result = fetch_weather(lat, lan, start_date, end_date)
    assert isinstance(result, pd.DataFrame)
    assert "time" in result.columns
    assert result["time"].dt.tz is not None
    assert "shortwave_radiation" in result.columns
    assert "cloud_cover" in result.columns
    assert "temperature_2m" in result.columns
    assert "wind_speed_10m" in result.columns
