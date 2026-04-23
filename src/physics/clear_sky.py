"""
Converting 02_eda.ipynb into a reusable module.
Two main functions are created here:
`compute_clear_sky(times)`
`compute_physics_pred(times)`
"""

# Import libraries and functions
import pandas as pd
from pvlib.location import Location

# Define the constants
GERMANY_LAT = 51.2
GERMANY_LON = 10.4
GERMANY_ALT = 200 #meter
SCALING_FACTOR = 37.5 # MW per W/m^2; calculated from 02_eda.ipynb notebook

def compute_clear_sky(times: pd.DatetimeIndex) -> pd.DataFrame:
    site = Location(GERMANY_LAT, GERMANY_LON, tz="UTC", altitude=200)
    # get the clear sky data which is a dataframe
    clearsky = site.get_clearsky(times)
    df = clearsky[["ghi"]].rename(columns={"ghi": "clear_sky_ghi"})
    return df

def compute_physics_pred(times: pd.DatetimeIndex) -> pd.Series:
    df_clearsky = compute_clear_sky(times)
    
    # compute physics predication
    physics_pred = df_clearsky["clear_sky_ghi"] * SCALING_FACTOR
    # rename the series
    physics_pred.name = "physics_pred"

    print(f"The First 10 rows of the series `physics_pred` is: \n{physics_pred.head()}")
    return physics_pred