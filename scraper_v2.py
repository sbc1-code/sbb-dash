#!/usr/bin/env python3
"""
Local business demand forecaster.

Generates a 7-day forecast for any US ZIP using live weather, day-of-week
patterns, and optional local event enrichments when a supported adapter exists.
Santa Barbara ZIPs keep the original local event adapters.
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta


MODEL_VERSION = "2026-06-05-general-zip-v1"
DEFAULT_ZIP = "93101"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 local-demand-forecaster/1.0"
)
ZIP_RE = re.compile(r"^\d{5}$")


def fetch_json(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url, timeout=10):
    headers = {"User-Agent": USER_AGENT}
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception as exc:
            print(f"  Warning: fetch attempt {attempt + 1}/3 failed for {url}: {exc}")
            if attempt < 2:
                time.sleep(2)
    return None


def validate_zip(zip_code):
    cleaned = str(zip_code or "").strip()
    if not ZIP_RE.match(cleaned):
        raise ValueError("ZIP must be exactly 5 digits")
    return cleaned


def geocode_zip(zip_code):
    """Resolve a US ZIP to city, state, latitude, and longitude."""
    zip_code = validate_zip(zip_code)
    url = f"https://api.zippopotam.us/us/{urllib.parse.quote(zip_code)}"
    data = fetch_json(url)
    places = data.get("places") or []
    if not places:
        raise ValueError(f"No location found for ZIP {zip_code}")

    place = places[0]
    lat = float(place["latitude"])
    lon = float(place["longitude"])
    return {
        "zip": zip_code,
        "city": place.get("place name", ""),
        "state": place.get("state", ""),
        "state_code": place.get("state abbreviation", ""),
        "country": data.get("country", "United States"),
        "latitude": lat,
        "longitude": lon,
        "label": f"{place.get('place name', zip_code)}, {place.get('state abbreviation', '').strip()} {zip_code}".strip(),
    }


def is_santa_barbara_location(location):
    city = (location.get("city") or "").lower()
    state_code = (location.get("state_code") or "").upper()
    return state_code == "CA" and (location.get("zip", "").startswith("931") or "santa barbara" in city)


def get_weather_forecast(location):
    """Get 7-day weather from Open-Meteo for a resolved location."""
    params = urllib.parse.urlencode(
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode",
            "temperature_unit": "fahrenheit",
            "timezone": "auto",
            "forecast_days": 7,
        }
    )
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    data = fetch_json(url)
    daily = data.get("daily")
    if not daily or len(daily.get("time", [])) < 7:
        raise ValueError("Open-Meteo returned incomplete daily forecast data")
    return daily


def get_next_7_days(weather=None):
    """Generate date metadata, preferring weather API dates when available."""
    days = []
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weather_dates = (weather or {}).get("time") or []

    for i in range(7):
        if i < len(weather_dates):
            date = datetime.strptime(weather_dates[i], "%Y-%m-%d")
        else:
            date = datetime.now() + timedelta(days=i)

        days.append(
            {
                "date": date.strftime("%Y-%m-%d"),
                "day_name": day_names[date.weekday()],
                "day_short": day_names[date.weekday()][:3].upper(),
                "day_of_week": date.weekday(),
                "is_weekend": date.weekday() >= 5,
                "month_day": date.strftime("%m/%d"),
            }
        )

    return days


class EventScraper:
    """Local event enrichments. Only Santa Barbara adapters are implemented."""

    @staticmethod
    def scrape_cruise_ships():
        print("Fetching Santa Barbara cruise ship data...")
        url = "https://www.cruisemapper.com/ports/santa-barbara-ca-port-852"
        html = fetch_text(url)
        if not html:
            print("  Cruise data unavailable")
            return []

        events = []
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        window_end = today + timedelta(days=14)
        false_positives = {
            "santa barbara",
            "port of",
            "california",
            "united states",
            "cruise ship",
            "cruisemapper",
            "privacy policy",
            "cookie",
        }

        def is_valid_ship_name(name):
            clean = name.strip().lower()
            return 4 <= len(clean) <= 40 and not any(fp in clean for fp in false_positives)

        patterns = [
            r"([A-Z][a-z]+(?:\s+(?:of\s+the\s+Seas|[A-Z][a-z]+)){1,4})\s*[^A-Za-z]*?(\d{4}-\d{2}-\d{2})",
            r"(\d{4}-\d{2}-\d{2})\s*[^A-Za-z]*?([A-Z][a-z]+(?:\s+(?:of\s+the\s+Seas|Princess|Lady|[A-Z][a-z]+)){1,3})",
        ]
        seen_dates = set()

        for pattern in patterns:
            for first, second in re.findall(pattern, html):
                date_str, ship_name = (second, first) if first[0].isalpha() else (first, second)
                try:
                    event_date = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    continue

                if today <= event_date <= window_end and date_str not in seen_dates and is_valid_ship_name(ship_name):
                    seen_dates.add(date_str)
                    events.append(
                        {
                            "date": date_str,
                            "name": f"{ship_name.strip()} Arrival",
                            "type": "cruise",
                            "impact": "high",
                            "estimated_visitors": 2000,
                        }
                    )

        print(f"  Cruise arrivals found: {len(events)}")
        return events

    @staticmethod
    def scrape_sb_bowl():
        print("Fetching Santa Barbara Bowl concerts...")
        url = "https://sbbowl.com/concerts/"
        html = fetch_text(url)
        if not html:
            print("  Concert data unavailable")
            return []

        events = []
        current_year = datetime.now().year
        month_map = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }

        for month_str, day_str, artist in re.findall(r"([A-Z][a-z]{2,8})\s+(\d{1,2}).*?([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})", html)[:10]:
            month = month_map.get(month_str[:3])
            if not month:
                continue
            try:
                event_date = datetime(current_year, month, int(day_str))
                if event_date < datetime.now():
                    event_date = datetime(current_year + 1, month, int(day_str))
            except ValueError:
                continue

            events.append(
                {
                    "date": event_date.strftime("%Y-%m-%d"),
                    "name": f"{artist} at SB Bowl",
                    "type": "concert",
                    "impact": "high",
                    "estimated_visitors": 4500,
                }
            )

        print(f"  Concerts found: {len(events)}")
        return events

    @staticmethod
    def get_static_santa_barbara_events():
        events = []
        today = datetime.now()
        for i in range(14):
            date = today + timedelta(days=i)
            if date.weekday() == 1:
                events.append(
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "name": "Downtown Santa Barbara Farmers Market",
                        "type": "market",
                        "impact": "medium",
                        "estimated_visitors": 500,
                    }
                )
            if date.weekday() == 5:
                events.append(
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "name": "Saturday Santa Barbara Farmers Market",
                        "type": "market",
                        "impact": "medium",
                        "estimated_visitors": 1000,
                    }
                )
        return events


def collect_events(location):
    if not is_santa_barbara_location(location):
        return [], "weather_and_calendar_only"

    events = EventScraper.get_static_santa_barbara_events()
    for fetcher in (EventScraper.scrape_cruise_ships, EventScraper.scrape_sb_bowl):
        try:
            events.extend(fetcher())
        except Exception as exc:
            print(f"  Warning: event adapter failed: {exc}")
    return events, "santa_barbara_enriched"


def calculate_demand_score(day, weather=None, events=None, weather_index=None):
    """Return score, level, factors, recommendation, and matching events."""
    score = 50
    factors = []

    if day["is_weekend"]:
        score += 25
        factors.append("Weekend traffic (+25)")
    elif day["day_of_week"] == 4:
        score += 15
        factors.append("Friday activity (+15)")
    elif day["day_of_week"] == 2:
        score += 5
        factors.append("Midweek activity (+5)")

    if weather is not None:
        try:
            idx = weather_index if weather_index is not None else weather["time"].index(day["date"])
            temp = weather["temperature_2m_max"][idx]
            rain_prob = weather["precipitation_probability_max"][idx]

            if 65 <= temp <= 82:
                score += 12
                factors.append(f"Ideal weather {int(temp)}F (+12)")
            elif 82 < temp <= 92:
                score -= 5
                factors.append(f"Hot weather {int(temp)}F (-5)")
            elif temp > 92:
                score -= 10
                factors.append(f"Extreme heat {int(temp)}F (-10)")
            elif temp < 45:
                score -= 10
                factors.append(f"Cold weather {int(temp)}F (-10)")
            elif temp < 60:
                score -= 5
                factors.append(f"Cool weather {int(temp)}F (-5)")

            if rain_prob > 60:
                score -= 20
                factors.append(f"{int(rain_prob)}% rain chance (-20)")
            elif rain_prob > 35:
                score -= 10
                factors.append(f"{int(rain_prob)}% rain chance (-10)")
        except (KeyError, ValueError, IndexError, TypeError) as exc:
            factors.append(f"Weather scoring unavailable ({exc})")

    day_events = [event for event in (events or []) if event.get("date") == day["date"]]
    for event in day_events:
        if event.get("impact") == "high":
            score += 25
            factors.append(f"{event['name']} (+25)")
        elif event.get("impact") == "medium":
            score += 15
            factors.append(f"{event['name']} (+15)")

    bounded = min(100, max(0, int(round(score))))
    if bounded >= 75:
        level = "HIGH"
        recommendation = "Staff up, protect inventory, and prep for heavier foot traffic"
    elif bounded >= 55:
        level = "MEDIUM"
        recommendation = "Use normal staffing and monitor afternoon demand"
    else:
        level = "LOW"
        recommendation = "Keep staffing lean and push targeted offers"

    return {
        "score": bounded,
        "level": level,
        "factors": factors,
        "recommendation": recommendation,
        "events": [{"name": e["name"], "type": e["type"]} for e in day_events],
    }


def build_forecast(location, weather, events):
    days = get_next_7_days(weather)
    forecast = []

    for idx, day in enumerate(days):
        demand = calculate_demand_score(day, weather, events, idx)
        forecast.append(
            {
                **day,
                "demand": demand,
                "weather": {
                    "temp_high": int(round(weather["temperature_2m_max"][idx])),
                    "temp_low": int(round(weather["temperature_2m_min"][idx])),
                    "rain_prob": int(round(weather["precipitation_probability_max"][idx])),
                },
            }
        )

    if len(forecast) != 7:
        raise ValueError("Forecast quality check failed: expected exactly 7 days")
    return forecast


def generate_forecast_data(zip_code=DEFAULT_ZIP):
    zip_code = validate_zip(zip_code or DEFAULT_ZIP)
    print("=" * 60)
    print("LOCAL BUSINESS DEMAND FORECAST GENERATOR")
    print("=" * 60)
    print(f"ZIP: {zip_code}")

    location = geocode_zip(zip_code)
    print(f"Location: {location['label']} ({location['latitude']}, {location['longitude']})")

    weather = get_weather_forecast(location)
    print("Weather: available")

    events, event_scope = collect_events(location)
    print(f"Events: {len(events)} ({event_scope})")

    forecast = build_forecast(location, weather, events)
    print("Quality checks: passed")

    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "model_version": MODEL_VERSION,
        "location": location,
        "forecast": forecast,
        "events": events,
        "data_quality": {
            "weather_available": True,
            "events_count": len(events),
            "event_scope": event_scope,
            "forecast_days": len(forecast),
            "sources": ["Zippopotam US ZIP geocoding", "Open-Meteo weather"]
            + (["Santa Barbara local event adapters"] if event_scope == "santa_barbara_enriched" else []),
        },
    }


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Generate a local business demand forecast for a US ZIP.")
    parser.add_argument("--zip", default=os.getenv("FORECAST_ZIP", DEFAULT_ZIP), help="US ZIP code to forecast")
    parser.add_argument("--output", default="forecast_data.json", help="Output JSON path")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv or sys.argv[1:])
    try:
        data = generate_forecast_data(args.zip)
    except (ValueError, urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"Fatal: could not generate forecast: {exc}", file=sys.stderr)
        return 1

    with open(args.output, "w", encoding="utf-8") as out:
        json.dump(data, out, indent=2)

    print("=" * 60)
    print("FORECAST GENERATED")
    print("=" * 60)
    print(f"Output: {args.output}")
    print(f"Days: {len(data['forecast'])}")
    print(f"Generated: {data['generated_at']}")
    for day in data["forecast"]:
        event_count = len(day["demand"]["events"])
        suffix = f" ({event_count} events)" if event_count else ""
        print(f"  {day['day_name']:9} {day['month_day']:5} -> {day['demand']['level']:6} ({day['demand']['score']:3}/100){suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
