import psycopg2  # the Python driver that speaks PostgreSQL's network protocol


DB_PARAMS = {
    "host": "localhost",   # container is exposed on the laptop via port mapping
    "port": 5432,          # PostgreSQL standard port
    "dbname": "solar_db",  # matches POSTGRES_DB in docker-compose.yml
    "user": "solar",       # matches POSTGRES_USER
    "password": "solar",   # matches POSTGRES_PASSWORD
}


def test_db_connection():
    """Can Python open a connection to TimescaleDB at all?"""
    conn = psycopg2.connect(**DB_PARAMS)  # ** unpacks the dict as keyword arguments
    conn.close()                          # always close: release the connection slot


def test_timescaledb_extension():
    """Is the TimescaleDB extension actually installed inside PostgreSQL?"""
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()                   # cursor = a handle for sending SQL commands
    cur.execute(
        "SELECT extname FROM pg_extension WHERE extname = 'timescaledb';"
    )
    row = cur.fetchone()                  # fetchone() returns first result row, or None
    cur.close()
    conn.close()
    assert row is not None, "TimescaleDB extension not found — did the image load correctly?"
