# Aurora Window

A live public dashboard for comparing tonight's northern-lights viewing conditions at ten established aurora destinations.

## Live method

For every dark forecast hour in the next 30 hours, the page calculates:

```
100 × sqrt((OVATION / 100) × min(Kp / 5, 1))
    × darkness
    × (1 - cloud_cover / 100)
    × min(visibility_metres / 10000, 1)
```

The displayed value is the highest-scoring hour. It is a transparent decision score on a 0–100 scale, **not a calibrated statistical probability or guarantee**.

- **OVATION:** nearest 1-degree cell from NOAA SWPC's 30–90 minute aurora forecast.
- **Kp:** nearest NOAA three-hour predicted Kp. Kp 5 is the denominator because it is NOAA's G1 storm threshold.
- **Darkness:** solar elevation factor, 0 at -6 degrees and 1 at -18 degrees, using NOAA's published solar-position approximation.
- **Cloud:** Open-Meteo total cloud cover.
- **Visibility:** Open-Meteo visibility, reaching its full factor at 10 km.
- **Tonight:** the best dark hour in the next 30 hours, converted to the location's timezone.

The geometric mean of OVATION and Kp is an explicit heuristic: OVATION supplies a location-specific short-term signal, while Kp supplies the broader forecast for the night. No public global API provides a calibrated per-town aurora probability combining space weather and terrestrial weather.

## Freshness and failure behavior

The browser fetches all live sources without cache every ten minutes. A score is hidden rather than shown as current when:

- NOAA OVATION is missing or its forecast time is more than three hours from the current time;
- NOAA Kp lacks at least 12 hours of future predicted coverage;
- Open-Meteo lacks a future hourly forecast for any spot; or
- any required request fails or times out.

No previous score is kept on screen after a failed refresh.

## Sources

- NOAA SWPC Aurora 30-Minute Forecast / OVATION: `https://services.swpc.noaa.gov/json/ovation_aurora_latest.json`
- NOAA SWPC Planetary K-index Forecast: `https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json`
- Open-Meteo Weather Forecast API: `https://api.open-meteo.com/v1/forecast`
- NOAA Global Monitoring Laboratory solar calculations: `https://gml.noaa.gov/grad/solcalc/calcdetails.html`
- Location coordinates and timezones: Open-Meteo Geocoding API, which documents GeoNames as its location database.
- Map boundaries: Natural Earth 110m Admin-0 Countries, public domain.

## Selected places

Fairbanks, Yellowknife, Churchill, Kangerlussuaq, Reykjavik, Tromso, Abisko, Rovaniemi, Kiruna and Longyearbyen. Coordinates in `app.js` were resolved from the Open-Meteo Geocoding API on October 18, 2026.

## Local use

Serve the folder over HTTP (not `file://`) so the browser can load `world.geojson`:

```
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Reproducible Kverna pipeline

`pipeline.json` is the exact exported Kverna pipeline. It fetches the two NOAA feeds and the batch Open-Meteo forecast, runs the documented Python calculation, and builds an auditable score table. Its schedule trigger is `0 */30 * * * *` (every 30 minutes). The browser dashboard independently refreshes its live sources every 10 minutes while open.
