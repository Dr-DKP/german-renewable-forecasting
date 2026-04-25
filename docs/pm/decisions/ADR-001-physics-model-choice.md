# ADR-001: Use pvlib Ineichen-Perez clear-sky model as physics baseline

**Status:** Accepted — 2026-04-23

---

## Context

The project thesis requires decomposing solar output into a physics-explainable component and a residual. We needed a clear-sky irradiance model for Germany (51.2°N, 10.4°E). The model must run offline (no NWP API dependency), cover 2022–2024 hourly, and produce GHI in W/m².

Three options were evaluated:

| Option | Pro | Con |
|---|---|---|
| Ineichen-Perez (pvlib) | Industry standard, validated for Europe, built-in Linke turbidity | Single-point, not spatially resolved |
| Simple latitude formula | Zero dependencies | Ignores atmosphere entirely, high error in winter |
| ERA5 reanalysis NWP | Spatially resolved, physically complete | Large download, complex setup — deferred to P3 scope |

## Decision

Use `pvlib.location.Location.get_clearsky()` with the Ineichen-Perez model. Scaling factor **37.5 MW/(W/m²)** derived from 2022–2024 mean ratio of actual solar output to clear-sky GHI during daylight hours.

## Consequences

- Physics baseline achieves **R² = 0.78**, **MAE = 3,856 MW** on daylight hours (2022–2024)
- Residual is the XGBoost learning target — 22% unexplained variance remains
- Limitation: single geographic point means spatial inhomogeneity (e.g. Bavaria clear, Hamburg overcast) is not captured — accepted for Germany aggregate scope
