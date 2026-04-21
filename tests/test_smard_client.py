"""
Tests smard_client.py if it is working as it should. all three modules should work.
get_available_timestamps(): returns a list? if it is non-empty and values are integeres.
fetch_chunk(ts): returns a DataFrame? Has `time` and `solar_mw` columns? time is `timezone` aware?
fetch_solar_generation(start,end): result is sorted by time? Dates are within the requested range? No nulls in time?
"""

# Import libraries
import pandas as pd
from src.data.smard_client import get_available_timestamps, fetch_chunk, fetch_solar_generation

def test_timestamps_returns_a_list():
    result = get_available_timestamps()
    assert isinstance(result,list)
    assert len(result) > 0
    assert isinstance(result[0], int)

def test_fetch_chunk():
    ts = get_available_timestamps()[-1]
    result = fetch_chunk(ts)
    assert isinstance(result, pd.DataFrame)
    assert "time" in result.columns
    assert "solar_mw" in result.columns
    assert result["time"].dt.tz is not None

def test_fetch_solar_generation():
    start = "2026-03-11"
    end = "2026-03-18"
    result = fetch_solar_generation(start,end)
    assert result["time"].is_monotonic_increasing # Is result sorted by time? 
    assert result["time"].min()>=pd.Timestamp(start, tz="UTC") # Is the earliest row within the start date?
    assert result["time"].notna().all() # Are there no nulls in time
