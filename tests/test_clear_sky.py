

# Import librariy(es) and modules
import pandas as pd
from src.physics.clear_sky import compute_clear_sky
# test1: if output length matches input length
def test_length_of_timestamps():
    times = pd.date_range("2024-06-21", periods=24, freq="h", tz="UTC")
    result = compute_clear_sky(times)
    assert len(result) == 24

# test2: if GHI (Global horizontal irradiance) is 0 at midnight in January
def test_ghi_zero_at_midnight_january():
    times = pd.date_range("2024-01-15 00:00", periods=1, freq="h", tz="UTC")
    result = compute_clear_sky(times)
    # check index location in clear_sky_ghi column
    assert result["clear_sky_ghi"].iloc[0] == 0 # 0 is the first row

# test 3: if GHI is not 0 at noon in June

def test_ghi_positive_at_noon_june():
    times = pd.date_range("2024-06-21 10:00", periods=1, freq="h", tz="UTC")
    # 10:00 UTC = 12:00 Berlin time (Summer)
    result = compute_clear_sky(times)
    assert result["clear_sky_ghi"].iloc[0] > 0