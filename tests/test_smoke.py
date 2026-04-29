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

def test_timescaledb_active_engine():
    """Can we actually query TimescaleDB metadata?"""
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    
    # This view only exists if TimescaleDB is active and working
    cur.execute("SELECT * FROM timescaledb_information.hypertables;")
    
    rows = cur.fetchall()
    assert len(rows) >= 2, f"Expected 2 hypertables, found {len(rows)}"

    cur.close()
    conn.close()

def test_hypertables_have_data():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM solar_generation;")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    assert count > 26000, f"Expected >26000 rows, got {count}"
