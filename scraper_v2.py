#!/usr/bin/env python3
"""
Santa Barbara Business Forecast - Advanced Scraper
Quality-assured, automated data collection with fallbacks
"""

import json
import urllib.request
import urllib.error
import re
from datetime import datetime, timedelta
from html.parser import HTMLParser
import time

class EventScraper:
    """Quality-assured web scraping with error handling"""

    @staticmethod
    def fetch_url(url, timeout=10):
        """Fetch URL with retry logic and error handling"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    return response.read().decode('utf-8')
            except Exception as e:
                print(f"  ⚠️  Attempt {attempt + 1}/3 failed: {e}")
                if attempt < 2:
                    time.sleep(2)
                else:
                    return None
        return None

    @staticmethod
    def scrape_cruise_ships():
        """
        Scrape cruise ship schedule from CruiseMapper
        Returns: list of {date, ship_name, passengers}
        """
        print("🚢 Scraping cruise ship data...")
        url = "https://www.cruisemapper.com/ports/santa-barbara-ca-port-852"

        html = EventScraper.fetch_url(url)
        if not html:
            print("  ❌ Failed to fetch cruise data, using fallback")
            return []

        events = []

        # Parse cruise schedule (basic regex approach)
        # CruiseMapper format: date patterns and ship names
        date_pattern = r'(\d{4}-\d{2}-\d{2})'
        dates = re.findall(date_pattern, html)

        # Look for ship names (typically in title case, 2-3 words)
        ship_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\s+\((?:arrives|departs)'
        ships = re.findall(ship_pattern, html, re.IGNORECASE)

        # Match dates with ships
        for i, date_str in enumerate(dates[:5]):  # Limit to next 5 arrivals
            try:
                ship_date = datetime.strptime(date_str, '%Y-%m-%d')
                ship_name = ships[i] if i < len(ships) else "Cruise Ship"

                events.append({
                    'date': date_str,
                    'name': f"{ship_name} Arrival",
                    'type': 'cruise',
                    'impact': 'high',
                    'estimated_visitors': 2000
                })
            except Exception as e:
                print(f"  ⚠️  Error parsing cruise: {e}")

        print(f"  ✅ Found {len(events)} cruise arrivals")
        return events

    @staticmethod
    def scrape_sb_bowl():
        """
        Scrape Santa Barbara Bowl concerts
        Returns: list of {date, artist, type}
        """
        print("🎵 Scraping SB Bowl concerts...")
        url = "https://sbbowl.com/concerts/"

        html = EventScraper.fetch_url(url)
        if not html:
            print("  ❌ Failed to fetch concert data, using fallback")
            return []

        events = []

        # Look for date patterns near artist names
        # SB Bowl typically uses formats like "Sep 26" or "September 26"
        concert_pattern = r'([A-Z][a-z]{2,8})\s+(\d{1,2}).*?([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})'
        matches = re.findall(concert_pattern, html)

        current_year = datetime.now().year

        for month_str, day_str, artist in matches[:10]:  # Limit to next 10 concerts
            try:
                # Parse date
                month_map = {
                    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
                }

                month = month_map.get(month_str[:3])
                if not month:
                    continue

                day = int(day_str)
                concert_date = datetime(current_year, month, day)

                # If date is in the past, assume next year
                if concert_date < datetime.now():
                    concert_date = datetime(current_year + 1, month, day)

                events.append({
                    'date': concert_date.strftime('%Y-%m-%d'),
                    'name': f"{artist} at SB Bowl",
                    'type': 'concert',
                    'impact': 'high',
                    'estimated_visitors': 4500
                })
            except Exception as e:
                print(f"  ⚠️  Error parsing concert: {e}")

        print(f"  ✅ Found {len(events)} concerts")
        return events

    @staticmethod
    def get_static_events():
        """
        Reliable fallback events that happen regularly
        """
        events = []

        # Weekly recurring events
        today = datetime.now()
        for i in range(14):  # Next 2 weeks
            date = today + timedelta(days=i)

            # Tuesday Farmers Market
            if date.weekday() == 1:
                events.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'name': 'Downtown Farmers Market',
                    'type': 'market',
                    'impact': 'medium',
                    'estimated_visitors': 500
                })

            # Saturday Farmers Market (larger)
            if date.weekday() == 5:
                events.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'name': 'Saturday Farmers Market',
                    'type': 'market',
                    'impact': 'medium',
                    'estimated_visitors': 1000
                })

        print(f"  ✅ Added {len(events)} recurring events")
        return events


def get_weather_forecast():
    """Get 7-day weather from Open-Meteo (free, no API key)"""
    print("🌤️  Fetching weather data...")
    url = "https://api.open-meteo.com/v1/forecast?latitude=34.4208&longitude=-119.6982&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode&temperature_unit=fahrenheit&timezone=America/Los_Angeles&forecast_days=7"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            print("  ✅ Weather data fetched")
            return data['daily']
    except Exception as e:
        print(f"  ❌ Weather fetch failed: {e}")
        return None


def get_next_7_days():
    """Generate next 7 days with metadata"""
    days = []
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        days.append({
            'date': date.strftime('%Y-%m-%d'),
            'day_name': day_names[date.weekday()],
            'day_short': day_names[date.weekday()][:3].upper(),
            'day_of_week': date.weekday(),
            'is_weekend': date.weekday() >= 5,
            'month_day': date.strftime('%m/%d')
        })

    return days


def calculate_demand_score(day, weather=None, events=None):
    """
    Enhanced demand scoring with event impact
    Returns: score (0-100), level (LOW/MEDIUM/HIGH), reasoning
    """
    score = 50  # baseline
    factors = []

    # Day of week impact
    if day['is_weekend']:
        score += 30
        factors.append("Weekend traffic (+30)")
    elif day['day_of_week'] == 4:  # Friday
        score += 20
        factors.append("Friday evening (+20)")
    elif day['day_of_week'] == 2:  # Wednesday
        score += 10
        factors.append("Midweek activity (+10)")

    # Weather impact
    if weather:
        try:
            idx = [d['date'] for d in get_next_7_days()].index(day['date'])
            temp = weather['temperature_2m_max'][idx]
            rain_prob = weather['precipitation_probability_max'][idx]

            # Perfect weather = higher demand
            if 65 <= temp <= 85:
                score += 15
                factors.append(f"Perfect weather {int(temp)}°F (+15)")
            elif temp > 85:
                score -= 5
                factors.append(f"Hot weather {int(temp)}°F (-5)")
            elif temp < 60:
                score -= 10
                factors.append(f"Cool weather {int(temp)}°F (-10)")

            # Rain = lower demand
            if rain_prob > 50:
                score -= 20
                factors.append(f"{rain_prob}% rain chance (-20)")
            elif rain_prob > 30:
                score -= 10
                factors.append(f"{rain_prob}% rain chance (-10)")
        except Exception as e:
            print(f"  ⚠️  Weather impact calculation error: {e}")

    # Event impact
    day_events = []
    if events:
        day_events = [e for e in events if e['date'] == day['date']]

        for event in day_events:
            if event['impact'] == 'high':
                boost = 25
                score += boost
                factors.append(f"{event['name']} (+{boost})")
            elif event['impact'] == 'medium':
                boost = 15
                score += boost
                factors.append(f"{event['name']} (+{boost})")

    # Determine level
    if score >= 75:
        level = "HIGH"
        recommendation = "🔥 Staff up, extend hours, maximize capacity"
    elif score >= 55:
        level = "MEDIUM"
        recommendation = "📊 Normal staffing, run targeted promotions"
    else:
        level = "LOW"
        recommendation = "💡 Minimal staff, push deals to locals"

    return {
        'score': min(100, max(0, int(score))),
        'level': level,
        'factors': factors,
        'recommendation': recommendation,
        'events': [{'name': e['name'], 'type': e['type']} for e in day_events]
    }


def generate_forecast_data():
    """
    Main function: generate complete forecast with quality checks
    """
    print("\n" + "="*60)
    print("🌴 SANTA BARBARA BUSINESS FORECAST GENERATOR")
    print("="*60 + "\n")

    # Fetch all data sources
    days = get_next_7_days()
    weather = get_weather_forecast()

    # Gather events from multiple sources
    all_events = []

    # Always include static/recurring events
    all_events.extend(EventScraper.get_static_events())

    # Try to scrape cruise ships (non-critical)
    try:
        cruise_events = EventScraper.scrape_cruise_ships()
        all_events.extend(cruise_events)
    except Exception as e:
        print(f"  ⚠️  Cruise scraping failed: {e}")

    # Try to scrape SB Bowl (non-critical)
    try:
        concert_events = EventScraper.scrape_sb_bowl()
        all_events.extend(concert_events)
    except Exception as e:
        print(f"  ⚠️  Concert scraping failed: {e}")

    print(f"\n📅 Total events collected: {len(all_events)}")

    # Generate forecast for each day
    forecast = []
    for day in days:
        demand = calculate_demand_score(day, weather, all_events)

        day_forecast = {
            **day,
            'demand': demand,
            'weather': {}
        }

        # Add weather data
        if weather:
            try:
                idx = days.index(day)
                day_forecast['weather'] = {
                    'temp_high': int(weather['temperature_2m_max'][idx]),
                    'temp_low': int(weather['temperature_2m_min'][idx]),
                    'rain_prob': weather['precipitation_probability_max'][idx]
                }
            except Exception as e:
                print(f"  ⚠️  Weather assignment error: {e}")

        forecast.append(day_forecast)

    # Quality check
    if not forecast or len(forecast) != 7:
        print("  ❌ QUALITY CHECK FAILED: Invalid forecast data")
        return None

    print("\n✅ QUALITY CHECKS PASSED")

    return {
        'generated_at': datetime.now().isoformat(),
        'forecast': forecast,
        'events': all_events,
        'data_quality': {
            'weather_available': weather is not None,
            'events_count': len(all_events),
            'forecast_days': len(forecast)
        }
    }


if __name__ == '__main__':
    data = generate_forecast_data()

    if not data:
        print("\n❌ FATAL ERROR: Could not generate forecast")
        exit(1)

    # Save to JSON
    with open('forecast_data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n{'='*60}")
    print("✅ FORECAST GENERATED SUCCESSFULLY")
    print(f"{'='*60}")
    print(f"📊 {len(data['forecast'])} days forecasted")
    print(f"🎉 {data['data_quality']['events_count']} events included")
    print(f"🌤️  Weather: {'✅' if data['data_quality']['weather_available'] else '❌'}")
    print(f"🕐 Generated: {data['generated_at']}")

    # Print summary
    print(f"\n📈 WEEK OVERVIEW:")
    print("-" * 60)
    for day in data['forecast']:
        events_str = f" ({len(day['demand']['events'])} events)" if day['demand']['events'] else ""
        print(f"  {day['day_name']:9} {day['month_day']:5} → {day['demand']['level']:6} ({day['demand']['score']:3}/100){events_str}")

    print(f"\n{'='*60}\n")
