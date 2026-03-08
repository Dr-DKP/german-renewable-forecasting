"""
SMARD API Client — Bundesnetzagentur electricity market data.

Fetches hourly generation data (solar, wind onshore, wind offshore)
from Germany's official Strommarktdaten platform.

API docs: https://www.smard.de/app/help/en
"""


def fetch_generation_data(start_date: str, end_date: str, sources: list[str]):
    """Fetch hourly generation data from SMARD API.

    Args:
        start_date: ISO format date string (e.g., '2018-01-01')
        end_date: ISO format date string (e.g., '2024-12-31')
        sources: List of generation sources ('solar', 'wind_onshore', 'wind_offshore')

    Returns:
        pd.DataFrame with datetime index and generation columns in MW.
    """
    raise NotImplementedError("Phase 0 — implementation in progress")
