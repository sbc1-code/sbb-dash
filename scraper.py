#!/usr/bin/env python3
"""
Santa Barbara Business Forecast Data Scraper
Pulls real data from public sources - 100% free
"""

import json
import urllib.request
from datetime import datetime, timedelta
from html.parser import HTMLParser

def get_weather_forecast():
    """Get 7-day weather from Open-Meteo (free, no API key)"""
    url = "https://api.open-meteo.com/v1/forecast?latitude=34.4208&longitude=-119.6982&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode&temperature_unit=fahrenheit&timezone=America/Los_Angeles&forecast_days=7"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            return data['daily']
    except Exception as e:
        print(f"Weather fetch failed: {e}")
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
            'day_of_week': date.weekday(),  # 0 = Monday
            'is_weekend': date.weekday() >= 5,
            'month_day': date.strftime('%m/%d')
        })

    return days

def calculate_demand_score(day, weather=None):
    """
    Smart demand scoring algorithm
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
        factors.append("Farmers Market day (+10)")

    # Weather impact
    if weather:
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

    # Determine level
    if score >= 75:
        level = "HIGH"
        recommendation = "Staff up, increase inventory, extend hours"
    elif score >= 55:
        level = "MEDIUM"
        recommendation = "Normal staffing, consider promotions"
    else:
        level = "LOW"
        recommendation = "Skeleton crew, push promotions to locals"

    return {
        'score': min(100, max(0, score)),
        'level': level,
        'factors': factors,
        'recommendation': recommendation
    }

def generate_forecast_data():
    """Main function: generate complete forecast data"""
    days = get_next_7_days()
    weather = get_weather_forecast()

    forecast = []
    for day in days:
        demand = calculate_demand_score(day, weather)

        day_forecast = {
            **day,
            'demand': demand,
            'weather': {}
        }

        # Add weather data
        if weather:
            idx = days.index(day)
            day_forecast['weather'] = {
                'temp_high': int(weather['temperature_2m_max'][idx]),
                'temp_low': int(weather['temperature_2m_min'][idx]),
                'rain_prob': weather['precipitation_probability_max'][idx]
            }

        forecast.append(day_forecast)

    return {
        'generated_at': datetime.now().isoformat(),
        'forecast': forecast
    }

if __name__ == '__main__':
    data = generate_forecast_data()

    # Save to JSON
    with open('forecast_data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print("✅ Forecast data generated!")
    print(f"📅 {len(data['forecast'])} days forecasted")
    print(f"🕐 Generated at: {data['generated_at']}")

    # Print summary
    print("\n📊 Week Overview:")
    for day in data['forecast']:
        print(f"  {day['day_name']:9} {day['month_day']:5} → {day['demand']['level']:6} ({day['demand']['score']}/100)")
