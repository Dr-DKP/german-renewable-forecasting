
-- Create Extension and regular tables from perquets data
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS solar_generation (
    time        TIMESTAMPTZ NOT NULL,
    solar_mw    DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS weather_observations (
    time                TIMESTAMPTZ NOT NULL,
    shortwave_radiation DOUBLE PRECISION,
    cloud_cover         DOUBLE PRECISION,
    temperature_2m      DOUBLE PRECISION,
    wind_speed_10m      DOUBLE PRECISION
);

-- Now convert both tables to hypertables
SELECT create_hypertable('solar_generation', 'time', if_not_exists => TRUE);
SELECT create_hypertable('weather_observations', 'time', if_not_exists => TRUE);
