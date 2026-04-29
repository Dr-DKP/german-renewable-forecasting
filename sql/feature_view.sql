
CREATE OR REPLACE VIEW feature_view AS

SELECT
    s.time,
    s.solar_mw,
    w.shortwave_radiation,
    w.cloud_cover,
    -- lag features (window functions)
    LAG(w.cloud_cover, 1)        OVER (ORDER BY s.time) AS cloud_cover_lag_1h,
    LAG(w.shortwave_radiation, 1) OVER (ORDER BY s.time) AS radiation_lag_1h,
    -- rolling 3h average
    AVG(w.cloud_cover) OVER (ORDER BY s.time ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS cloud_cover_rolling_3h,
    -- time encodings
    EXTRACT(HOUR  FROM s.time) AS hour,
    EXTRACT(MONTH FROM s.time) AS month
FROM solar_generation s
JOIN weather_observations w ON s.time = w.time
ORDER BY s.time;
