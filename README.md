# Local Business Demand Forecaster

Free 7-day demand forecasts for any US ZIP. The public page runs as a static GitHub Pages app and uses live browser-side ZIP geocoding plus Open-Meteo weather for custom locations.

**Live demo:** <https://sbc1-code.github.io/sbb-dash/>

## What It Does

- Accepts any valid 5-digit US ZIP.
- Resolves the ZIP to city, state, latitude, and longitude with Zippopotam.
- Fetches a 7-day weather forecast from Open-Meteo.
- Scores each day from 0-100 using day-of-week, temperature, rain probability, and event signals.
- Produces practical staffing/inventory guidance for high, medium, and low demand days.
- Keeps Santa Barbara-specific event enrichment only for Santa Barbara ZIPs.

For non-Santa Barbara ZIPs, the model is honest: it uses live weather plus calendar patterns and does not invent local event data.

## Data Sources

- **Zippopotam:** US ZIP geocoding.
- **Open-Meteo:** no-key weather forecast.
- **Santa Barbara adapters:** recurring farmers markets, cruise arrivals, and SB Bowl concerts when available.

## Score Model

Baseline score starts at 50.

- Weekend: +25
- Friday: +15
- Wednesday: +5
- Ideal high temperature, 65-82F: +12
- Hot, cold, and rainy weather reduce the score
- Medium event: +15
- High event: +25
- Scores are capped from 0 to 100

This is a planning signal, not a guarantee of sales or foot traffic.

## Run Locally

Open the static app:

```bash
python3 -m http.server 8000
```

Then visit:

```text
http://localhost:8000/forecast.html?zip=10001
```

Generate checked-in JSON for a ZIP:

```bash
python3 scraper_v2.py --zip 93101 --output forecast_data.json
```

Run tests:

```bash
python3 -m unittest discover -s tests
```

## GitHub Actions

`.github/workflows/update-forecast.yml` refreshes `forecast_data.json` daily for the default ZIP (`93101`). Manual workflow runs accept a `zip` input if the checked-in default should be regenerated for another location.

## Files

```text
index.html            Landing entry with ZIP form
forecast.html         Static ZIP forecaster app
forecast_data.json    Checked-in default forecast
scraper_v2.py         ZIP-aware forecast generator
scraper.py            Compatibility wrapper
tests/                Scoring and validation tests
```

## License

MIT
